from math import radians, sin, cos, asin, sqrt
from typing import List, Tuple
import requests
from app.models.schemas import RouteRequest, RouteResponse, RouteSegment

# Zonas ficticias para el MVP (coordenadas aprox)
TOLL_ZONES = [(-33.45, -70.65, 5.0, 3.5)]  # Santiago: radio 5 km, peaje 3.5
RISK_ZONES = [(-33.03, -71.55, 6.0, 0.6)]  # Viña: radio 6 km, riesgo 0.6

# ------------------- AUXILIARES -------------------

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*asin(sqrt(a))

def point_distance_km(p, c):
    return haversine_km(p[0], p[1], c[0], c[1])

def crosses_zone(path: List[Tuple[float, float]], zone):
    zlat, zlon, radius_km, _ = zone
    for pt in path:
        if point_distance_km(pt, (zlat, zlon)) <= radius_km:
            return True
    return False

def interpolate_path(a: Tuple[float, float], b: Tuple[float, float], steps=20):
    lat1, lon1 = a
    lat2, lon2 = b
    return [
        (lat1 + (lat2 - lat1) * i / steps, lon1 + (lon2 - lon1) * i / steps)
        for i in range(steps + 1)
    ]

def format_duration_hm(minutes: float) -> str:
    """Convierte minutos a 'H:MM' (ej: 1:40 para 1h 40min)."""
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}:{mins:02d}"

# ------------------- FALLBACK (línea recta) -------------------

def _fallback_straight_route(req: RouteRequest) -> RouteResponse:
    path = interpolate_path((req.origin.lat, req.origin.lon),
                            (req.destination.lat, req.destination.lon))
    dist = 0.0
    for i in range(len(path) - 1):
        dist += haversine_km(path[i][0], path[i][1], path[i+1][0], path[i+1][1])

    toll = sum(z[3] for z in TOLL_ZONES if crosses_zone(path, z))
    risk = sum(z[3] for z in RISK_ZONES if crosses_zone(path, z))
    duration_min = dist / 80 * 60  # estimado: 80 km/h

    return RouteResponse(
        distance_km=round(dist, 2),
        toll_cost=round(toll, 2),
        risk_score=round(risk, 2),
        duration_min=format_duration_hm(duration_min),
        path=RouteSegment(coords=path)
    )

# ------------------- PRINCIPAL (OSRM) -------------------

def optimize_route(req: RouteRequest) -> RouteResponse:
    """
    Usa OSRM (servidor público) para obtener ruta por carretera.
    Si falla (sin internet/limit), usa fallback a línea recta.
    """
    try:
        orig = (req.origin.lat, req.origin.lon)
        dest = (req.destination.lat, req.destination.lon)

        # OSRM espera (lon,lat) y devuelve geojson con coordinates = [[lon,lat], ...]
        url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{orig[1]},{orig[0]};{dest[1]},{dest[0]}"
            f"?overview=full&geometries=geojson"
        )

        r = requests.get(url, timeout=10)
        data = r.json()

        if r.status_code != 200 or data.get("code") != "Ok":
            return _fallback_straight_route(req)

        route = data["routes"][0]
        coords = [(lnglat[1], lnglat[0]) for lnglat in route["geometry"]["coordinates"]]
        dist_km = route["distance"] / 1000.0
        duration_minutes = route["duration"] / 60.0

        toll = sum(z[3] for z in TOLL_ZONES if crosses_zone(coords, z))
        risk = sum(z[3] for z in RISK_ZONES if crosses_zone(coords, z))

        return RouteResponse(
            distance_km=round(dist_km, 2),
            toll_cost=round(toll, 2),
            risk_score=round(risk, 2),
            duration_min=format_duration_hm(duration_minutes),
            path=RouteSegment(coords=coords)
        )

    except Exception:
        # No rompemos la demo: devolvemos línea recta
        return _fallback_straight_route(req)

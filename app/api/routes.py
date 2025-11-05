# app/api/routes.py
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import RouteRequest
from app.services.route_service import optimize_route
import requests
from app.db.conn import get_db
import sqlite3

router = APIRouter()


def _ensure_history_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS route_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin_text TEXT,
            destination_text TEXT,
            origin_lat REAL,
            origin_lon REAL,
            destination_lat REAL,
            destination_lon REAL,
            distance_km REAL,
            duration_min TEXT,
            risk_score REAL,
            toll_cost REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

@router.post("/optimize")
def optimize(
    req: RouteRequest,
    origin_text: str | None = Query(None),
    destination_text: str | None = Query(None),
):
    """
    Calcula ruta óptima entre origen y destino (lat/lon).
    """
    try:
        result = optimize_route(req)

        # Registrar en historial
        try:
            conn = get_db()
            cur = conn.cursor()
            _ensure_history_table(cur)
            cur.execute(
                """
                INSERT INTO route_history (
                    origin_text, destination_text,
                    origin_lat, origin_lon, destination_lat, destination_lon,
                    distance_km, duration_min, risk_score, toll_cost
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    origin_text,
                    destination_text,
                    req.origin.lat,
                    req.origin.lon,
                    req.destination.lat,
                    req.destination.lon,
                    result.distance_km,
                    result.duration_min,
                    result.risk_score,
                    result.toll_cost,
                ),
            )
            conn.commit()
        except Exception:
            # No interrumpir la operación si el historial falla
            pass

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geocode")
def geocode(q: str = Query(..., min_length=3)):
    """
    Convierte una dirección a {lat, lon} usando Nominatim (OSM) — demo.
    """
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "LuxChile-MVP/1.0"}
    params = {"q": q, "format": "json", "limit": 1, "addressdetails": 0}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Geocoder externo no disponible")
    data = r.json()
    if not data:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}


@router.get("/recent")
def recent_routes(limit: int = Query(5, ge=1, le=50)):
    """
    Devuelve historial de rutas más recientes.
    """
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    _ensure_history_table(cur)
    cur.execute(
        """
        SELECT id, origin_text, destination_text,
               origin_lat, origin_lon, destination_lat, destination_lon,
               distance_km, duration_min, risk_score, toll_cost, created_at
        FROM route_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    return [dict(r) for r in cur.fetchall()]


@router.delete("/recent/{item_id}")
def delete_recent_route(item_id: int):
    """Elimina una entrada del historial de rutas."""
    conn = get_db()
    cur = conn.cursor()
    _ensure_history_table(cur)
    cur.execute("DELETE FROM route_history WHERE id = ?", (item_id,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(404, detail="Registro no encontrado")
    return {"deleted": True, "id": item_id}

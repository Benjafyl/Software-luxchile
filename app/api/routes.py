from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.models.schemas import RouteRequest
from app.services.route_service import optimize_route

router = APIRouter(prefix="/routes", tags=["routes"])

@router.post("/optimize")
def optimize(body: RouteRequest):
    return optimize_route(body)

@router.get("/demo_map", response_class=HTMLResponse)
def demo_map():
    # Mini UI con Leaflet para la demo
    return """
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>Demo Ruta</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style> #map{height:90vh;} body{margin:0;font-family:system-ui} </style>
</head>
<body>
<h3 style="margin:8px 12px">Demo – Optimización de Ruta (MVP)</h3>
<div id="map"></div>
<script>
const origin = {lat:-33.4475, lon:-70.6736};      // Santiago aprox
const destination = {lat:-33.0153, lon:-71.55};   // Viña del Mar aprox

async function fetchRoute(){
  const res = await fetch('/routes/optimize', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ origin, destination })
  });
  return await res.json();
}

async function init(){
  const m = L.map('map').setView([origin.lat, origin.lon], 8);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19}).addTo(m);

  const data = await fetchRoute();
  const latlngs = data.path.coords.map(c => [c[0], c[1]]);
  const line = L.polyline(latlngs).addTo(m);
  m.fitBounds(line.getBounds());

  L.marker([origin.lat, origin.lon]).addTo(m).bindPopup('Origen');
  L.marker([destination.lat, destination.lon]).addTo(m).bindPopup('Destino');
}
init();
</script>
</body>
</html>
"""

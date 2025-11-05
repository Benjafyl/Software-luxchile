# 🚛 LuxChile — Sistema de Gestión y Logística Inteligente

LuxChile es una plataforma web desarrollada con **React + FastAPI** para optimizar la gestión de stock, rutas y registro de incidentes en operaciones logísticas de transporte de lujo.  
Diseñada con una estética moderna, corporativa y centrada en la eficiencia, LuxChile busca digitalizar y automatizar los procesos internos de control logístico, brindando visibilidad y trazabilidad total en tiempo real.

---

## 🧩 Características Principales

### 🔹 Panel de Control (Frontend React)
- Interfaz moderna, minimalista y responsiva.
- Dashboard principal con acceso directo a cada módulo.
- Formularios optimizados para flujo rápido de datos.
- Paleta de colores corporativa (tonos grises y azul profesional).
- Integración con mapas dinámicos (Leaflet) y backend en tiempo real.

### 🔹 Módulos Disponibles
#### 📦 Consultar Stock
Permite visualizar en tiempo real la disponibilidad de productos en distintas bodegas.  
- Consulta por SKU.  
- Estados dinámicos (“Bajo stock”, “Disponible”).  
- Visualización clara y moderna con diseño corporativo.

#### 🗺️ Optimización de Rutas
Calcula rutas entre dos direcciones utilizando geocodificación automática y optimización desde FastAPI.  
- Ingreso de direcciones simples (sin coordenadas).  
- Resultado con distancia, duración y nivel de riesgo.  
- Mapa interactivo de ruta con marcadores de origen y destino.

#### ⚠️ Registro de Incidentes
Formulario rápido y estandarizado para reportar eventos de transporte.  
- ID de carga y RUT del conductor.  
- Selección de tipo de incidente (accidente, robo, desviación, etc.).  
- Registro geolocalizado con mensaje visual de confirmación.

---

## ⚙️ Tecnologías Utilizadas

### 🔸 Frontend
- **React + Vite**
- **TailwindCSS**
- **Leaflet.js**
- **JavaScript (ES2023)**

### 🔸 Backend
- **FastAPI (Python)**
- **SQLite / PostgreSQL**
- **Uvicorn**
- **Pydantic**

### 🔸 Infraestructura y Control
- **GitHub** (gestión de versiones)
- **PowerShell / Git Bash** (flujo de despliegue local)
- **Entorno local con Vite y Uvicorn**

---

## 🧱 Estructura del Proyecto
```
Software-luxchile/
├─ app/
│  ├─ api/
│  │  ├─ stock.py               # Endpoints de inventario
│  │  ├─ routes.py              # Endpoints de rutas + historial
│  │  ├─ incidents.py           # Endpoints de incidentes + listado/DELETE
│  │  ├─ asignaciones.py        # Endpoints de asignaciones (SQLAlchemy)
│  │  └─ schemas_asignaciones.py
│  ├─ services/
│  │  ├─ stock_service.py
│  │  ├─ route_service.py       # Cálculo OSRM + fallback, HH:MM:SS y CLP
│  │  └─ incident_service.py
│  ├─ models/
│  │  ├─ schemas.py             # Pydantic (requests/responses)
│  │  └─ asignaciones.py        # Modelos SQLAlchemy
│  ├─ db/
│  │  ├─ conn.py                # Conexión sqlite3 simple
│  │  ├─ database.py            # Engine SQLAlchemy (asignaciones)
│  │  └─ init_db.py             # Semilla de datos (inventario e incidentes)
│  ├─ core/config.py            # DB_PATH y configuración simple
│  └─ main.py                   # FastAPI app + CORS + routers
├─ frontend/
│  ├─ src/
│  │  └─ App.jsx                # SPA React (stock, rutas, incidentes, asignaciones)
│  └─ index.html
├─ start-dev.ps1                # Levanta backend y frontend en Windows
├─ requirements.txt             # Dependencias Python
└─ README.md
```

---

## 🚀 Puesta en Marcha

### Opción 1: Script (Windows)
- Ejecuta: `./start-dev.ps1`
  - Crea `.env` del frontend con `VITE_API_BASE=http://127.0.0.1:8000` si no existe
  - Abre dos ventanas (backend y frontend) y el navegador en `http://localhost:5173`

### Opción 2: Manual
1) Backend
- `python -m venv .venv`
- `./.venv/Scripts/Activate.ps1`
- `pip install -r requirements.txt`
- Inicializa la BD (carga SKUs 001–005): `python -m app.db.init_db`
- Arranca: `uvicorn app.main:app --reload`

2) Frontend
- `cd frontend`
- `npm install`
- `npm run dev`

---

## 🔧 Variables de Entorno
- `DB_PATH`: ruta del archivo SQLite (por defecto `inventario.db` en la raíz)
- Frontend: `VITE_API_BASE` (creado por `start-dev.ps1`)

Ejemplo PowerShell (usar ruta personalizada):
```
$env:DB_PATH = 'C:\ruta\inventario.db'
python -m app.db.init_db
uvicorn app.main:app --reload
```

---

## 🧠 API Principal (resumen)

Inventario
- `POST /stock/consultar` → body `{ sku }` → stock por bodega y estado

Rutas
- `POST /routes/optimize` → body `{ origin{lat,lon}, destination{lat,lon} }`
  - Query opcional: `origin_text`, `destination_text` (guardado en historial)
  - Respuesta incluye: `distance_km`, `duration_min`, `duration_hms`, `risk_score`, `toll_cost`, `toll_cost_clp`, `path`
- `GET /routes/geocode?q=texto` → `{ lat, lon }`
- `GET /routes/recent?limit=5` → historial (origen/destino, distancia, duración, riesgo, peaje)
- `DELETE /routes/recent/{id}` → elimina una entrada del historial

Incidentes
- `POST /incidentes/registrar` → crea incidente geolocalizado
- `GET /incidentes?limit=5` → últimos incidentes con `created_at`
- `DELETE /incidentes/{id}` → elimina incidente por id

Asignaciones
- `POST /asignaciones` → crea asignación; acepta payload “bonito” y alias legacy
- `GET /asignaciones` → lista recientes (SQLAlchemy)

---

## 🧮 Cálculo de Rutas y Peajes (MVP)
- La ruta se obtiene con OSRM (servidor público); si falla, fallback en línea recta.
- Peajes: se define un conjunto de zonas circulares (`TOLL_ZONES`), y si la ruta cruza una, se suma su costo.
- Conversión a CLP: `toll_cost_clp = toll_unidades × TOLL_UNIT_TO_CLP` (constante default: 1000 CLP por unidad).
- Duración devuelta también en `HH:MM:SS` para presentación.

Puedes ajustar en `app/services/route_service.py`:
- `TOLL_ZONES` (coordenadas, radio y costo de cada peaje)
- `TOLL_UNIT_TO_CLP` (factor de conversión a CLP)

---

## 🧪 Semilla de Datos
Ejecuta la semilla para cargar inventario de ejemplo (SKU001–SKU005) y crear tablas base:
```
python -m app.db.init_db
```

---

## 🛡️ Notas
- CORS habilitado para `http://localhost:5173`
- El frontend muestra en “Inicio” actividad reciente (incidentes y rutas) y permite ir al histórico completo
- Se pueden eliminar incidencias y entradas del historial de rutas desde la UI

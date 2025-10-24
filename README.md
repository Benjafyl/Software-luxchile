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


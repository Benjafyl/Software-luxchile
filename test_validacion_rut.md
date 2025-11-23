# Pruebas de Validación de RUT en Incidentes

## ✅ Implementación Completada

### 1. **Problema de CORS Resuelto**
- Se agregaron los puertos `8000` y `127.0.0.1:8000` a la configuración CORS en `main.py`
- Ahora el frontend puede comunicarse correctamente con el backend

### 2. **Validación de RUT Implementada**

#### Funcionalidad
El sistema ahora valida que el RUT ingresado al registrar un incidente corresponda al conductor asignado a esa carga.

#### Flujo de Validación
1. El usuario intenta registrar un incidente con:
   - `cargo_id`: ID de la carga
   - `employee_id`: RUT del conductor (formato: 12345678-9)
   - Otros datos del incidente

2. El sistema busca la asignación más reciente para ese `cargo_id`

3. Verifica que:
   - Exista una asignación para esa carga
   - La asignación tenga un responsable asignado
   - El RUT ingresado coincida con el RUT del responsable asignado

4. Si la validación falla, retorna error 403 con mensaje descriptivo

5. Si la validación pasa, registra el incidente normalmente

#### Archivos Modificados

1. **`app/main.py`**
   - Agregados puertos adicionales a CORS

2. **`app/api/asignaciones.py`**
   - Nueva función: `validar_rut_conductor_en_asignacion()`
   - Nuevo endpoint: `GET /asignaciones/cargo/{cargo_id}` para consultar asignaciones

3. **`app/services/incident_service.py`**
   - Actualizado `registrar_incidente()` con validación de RUT
   - Importa validación desde asignaciones

4. **`app/models/schemas.py`**
   - Mejorada documentación del campo `employee_id`

---

## 📋 Cómo Probar

### Paso 1: Crear una Asignación
```bash
POST http://localhost:8000/asignaciones
Content-Type: application/json
Authorization: Bearer <token_admin>

{
  "cargo_id": "CARGA-001",
  "vehicle_id": "CAMION-88",
  "prioridad": "ALTA",
  "origen": "Santiago",
  "destino": "Valparaíso",
  "responsable": {
    "rut": "12345678-9",
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "+56912345678"
  }
}
```

### Paso 2: Verificar la Asignación
```bash
GET http://localhost:8000/asignaciones/cargo/CARGA-001
Authorization: Bearer <token>
```

### Paso 3: Registrar Incidente con RUT Correcto ✅
```bash
POST http://localhost:8000/incidentes/registrar
Content-Type: application/json
Authorization: Bearer <token>

{
  "cargo_id": "CARGA-001",
  "vehicle_id": "CAMION-88",
  "employee_id": "12345678-9",
  "type": "DESVIO_RUTA",
  "description": "Desvío por obras en la ruta",
  "location": {
    "lat": -33.4489,
    "lon": -70.6693
  }
}
```

**Respuesta esperada (200 OK):**
```json
{
  "id": 1,
  "cargo_id": "CARGA-001",
  "vehicle_id": "CAMION-88",
  "employee_id": "12345678-9",
  "type": "DESVIO_RUTA",
  "description": "Desvío por obras en la ruta",
  "location": {"lat": -33.4489, "lon": -70.6693},
  "status": "ok",
  "validated": true,
  "message": "Incidente registrado correctamente. RUT validado."
}
```

### Paso 4: Intentar con RUT Incorrecto ❌
```bash
POST http://localhost:8000/incidentes/registrar
Content-Type: application/json
Authorization: Bearer <token>

{
  "cargo_id": "CARGA-001",
  "vehicle_id": "CAMION-88",
  "employee_id": "98765432-1",
  "type": "DESVIO_RUTA",
  "description": "Intento con RUT no autorizado",
  "location": {
    "lat": -33.4489,
    "lon": -70.6693
  }
}
```

**Respuesta esperada (403 Forbidden):**
```json
{
  "detail": {
    "error": "RUT_NO_AUTORIZADO",
    "message": "RUT no autorizado. El conductor asignado a la carga CARGA-001 es Juan Pérez (RUT: 12345678-9). RUT ingresado: 98765432-1",
    "cargo_id": "CARGA-001",
    "employee_id": "98765432-1"
  }
}
```

### Paso 5: Intentar con Carga No Asignada ❌
```bash
POST http://localhost:8000/incidentes/registrar
Content-Type: application/json
Authorization: Bearer <token>

{
  "cargo_id": "CARGA-999",
  "vehicle_id": "CAMION-88",
  "employee_id": "12345678-9",
  "type": "DESVIO_RUTA",
  "description": "Carga inexistente",
  "location": {
    "lat": -33.4489,
    "lon": -70.6693
  }
}
```

**Respuesta esperada (403 Forbidden):**
```json
{
  "detail": {
    "error": "RUT_NO_AUTORIZADO",
    "message": "No existe asignación para la carga CARGA-999",
    "cargo_id": "CARGA-999",
    "employee_id": "12345678-9"
  }
}
```

---

## 🎯 Beneficios de la Implementación

1. **Seguridad**: Previene suplantación de identidad
2. **Integridad de Datos**: Garantiza que solo el conductor asignado pueda registrar incidentes
3. **Trazabilidad**: Valida la relación entre conductor, carga e incidente
4. **Mensajes Claros**: Errores descriptivos para el usuario
5. **Auditabilidad**: Respuestas incluyen información de validación

---

## 🔧 Nuevos Endpoints Disponibles

### GET `/asignaciones/cargo/{cargo_id}`
Consulta la asignación activa para una carga específica.

**Ejemplo:**
```bash
GET http://localhost:8000/asignaciones/cargo/CARGA-001
```

**Respuesta:**
```json
{
  "id": 1,
  "cargo_id": "CARGA-001",
  "vehicle_id": "CAMION-88",
  "prioridad": "ALTA",
  "origen": "Santiago",
  "destino": "Valparaíso",
  "fecha_hora": "2025-11-20T10:00:00",
  "notas": null,
  "responsable_id": 1,
  "responsable": {
    "id": 1,
    "nombre": "Juan Pérez",
    "rut": "12345678-9",
    "telefono": "+56912345678",
    "email": "juan@example.com"
  }
}
```

---

## 📝 Notas Importantes

1. **Formato del RUT**: Debe ser sin puntos y con guión (ej: `12345678-9`)
2. **Case Insensitive**: El sistema normaliza los RUT a mayúsculas
3. **Asignación Más Reciente**: Si hay múltiples asignaciones, se usa la última
4. **Permisos**: Workers solo ven sus propias asignaciones

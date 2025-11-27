# Guía de Generación de PDFs

## ✅ Implementación Completa

Se han agregado botones para generar PDFs en dos vistas:

### 📋 Vista de Asignaciones de Carga
- **Ubicación**: Sección "Asignaciones recientes"
- **Botón**: Verde con ícono 📄 "Generar PDF"
- **Función**: `generateAsignacionesPDF(items)`
- **Contenido del PDF**:
  - Título: "Reporte de Asignaciones de Carga"
  - Fecha de generación
  - Tabla con: Cargo ID, Vehículo, Prioridad, Origen, Destino, Responsable, Fecha/Hora
  - Total de asignaciones
  - Nombre archivo: `asignaciones_[timestamp].pdf`

### 🚨 Vista de Histórico de Incidentes
- **Ubicación**: Header junto al botón "Actualizar"
- **Botón**: Verde con ícono 📄 "PDF"
- **Función**: `generateIncidentesPDF(items)`
- **Contenido del PDF**:
  - Título: "Reporte de Incidentes"
  - Fecha de generación
  - Tabla con: Cargo ID, Vehículo, RUT Empleado, Tipo, Descripción, Fecha/Hora
  - Total de incidentes
  - Resumen por tipo de incidente
  - Nombre archivo: `incidentes_[timestamp].pdf`

## 📦 Dependencias Instaladas
- `jspdf`: ^2.5.2
- `jspdf-autotable`: ^3.8.4

## 🎨 Características de los PDFs
- **Diseño profesional** con colores corporativos
- **Tablas responsivas** con formato automático
- **Paginación automática** para reportes grandes
- **Números de página** en footer
- **Alternancia de colores** en filas para mejor lectura
- **Resumen estadístico** al final del documento

## 🚀 Cómo Usar
1. Accede a la vista de Asignaciones o Incidentes
2. El botón PDF solo aparecerá si hay datos en la tabla
3. Haz clic en el botón "Generar PDF" o "PDF"
4. El PDF se descargará automáticamente

## ⚠️ Notas Importantes
- Los botones solo se muestran cuando hay datos disponibles
- El código existente NO fue modificado, solo se agregaron funcionalidades
- Los PDFs usan formato chileno para fechas (es-CL)
- Las descripciones largas se truncan automáticamente para mantener el formato

# Script para subir las ramas LC-2 y LC-3 a GitHub

## Método 1: Push directo (si tienes permisos)

### Paso 1: Autenticarse
Necesitas generar un Personal Access Token de GitHub:
1. Ve a: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Nombre: `luxchile-deploy`
4. Scope: Marca ✅ `repo`
5. Click "Generate token"
6. **COPIA EL TOKEN**

### Paso 2: Push rama LC-3
```powershell
git checkout feature/lc-3-dashboard-tiempo-real
git push https://TU_USUARIO:TU_TOKEN@github.com/benjita-unab/Software-luxchile.git feature/lc-3-dashboard-tiempo-real
```

### Paso 3: Push rama LC-2
```powershell
git checkout feature/lc-2-listado-stock-completo
git push https://TU_USUARIO:TU_TOKEN@github.com/benjita-unab/Software-luxchile.git feature/lc-2-listado-stock-completo
```

---

## Método 2: Usar bundle (alternativa)

Si no puedes hacer push directo, usa el archivo `luxchile-features.bundle`:

### En tu máquina con acceso:
```bash
# 1. Clonar el repo
git clone https://github.com/benjita-unab/Software-luxchile.git
cd Software-luxchile

# 2. Importar las ramas del bundle
git bundle unbundle ../luxchile-features.bundle

# 3. Push de ambas ramas
git push origin feature/lc-3-dashboard-tiempo-real
git push origin feature/lc-2-listado-stock-completo
```

---

## Método 3: GitHub Desktop (más fácil)

1. Abre GitHub Desktop
2. File → Add Local Repository → Selecciona `C:\Users\fesal\Software-luxchile`
3. En "Current Branch" selecciona `feature/lc-3-dashboard-tiempo-real`
4. Click "Publish branch" o "Push origin"
5. Repite para `feature/lc-2-listado-stock-completo`

---

## Estado Actual

### ✅ Rama LC-3: feature/lc-3-dashboard-tiempo-real
**Commit:** `b9f3d4e - feat(LC-3): Implementar dashboard con indicadores en tiempo real`

**Archivos incluidos (57):**
- Docker setup completo (7 archivos)
- Endpoint `/dashboard/kpis` (nuevo)
- Sistema de asignaciones con estados (modificado)
- Botón "Completar" en asignaciones
- Badge "Datos en tiempo real"
- Manejo automático de tokens expirados
- Documentación Docker completa

### ✅ Rama LC-2: feature/lc-2-listado-stock-completo
**Commit:** `da821e1 - feat(LC-2): Implementar listado completo de stock en interfaz`

**Archivos incluidos (7 adicionales a LC-3):**
- Endpoint `/stock/listado` (nuevo)
- Vista con tabs en página Stock (modificado)
- Tabla con listado completo de inventario
- Filtros: SKU, bodega, bajo stock
- KPIs de inventario
- Script de datos de prueba (6 registros)
- Inicialización automática de inventario

---

## Crear Pull Requests

Una vez subidas las ramas, crear PRs en GitHub:

### PR para LC-3:
1. Ve a: https://github.com/benjita-unab/Software-luxchile/compare
2. Base: `main` ← Compare: `feature/lc-3-dashboard-tiempo-real`
3. Título: `[LC-3] Dashboard con indicadores en tiempo real`
4. Descripción:
   ```
   ## Historia de Usuario LC-3
   Como Administrador quiero visualizar indicadores basados en datos en tiempo real 
   de la base de datos, para tomar decisiones operativas basadas en la situación 
   actual de la flota y no en datos de prueba.
   
   ## Cambios Implementados
   - ✅ Endpoint /dashboard/kpis con datos reales
   - ✅ KPIs: Órdenes en tránsito, Incidentes, Duración promedio, SLA
   - ✅ Sistema de completar asignaciones
   - ✅ Estados de asignaciones (ASIGNADA, EN_CURSO, COMPLETADA)
   - ✅ Cálculo de SLA real
   - ✅ Docker setup completo
   - ✅ Manejo de tokens expirados
   ```

### PR para LC-2:
1. Ve a: https://github.com/benjita-unab/Software-luxchile/compare
2. Base: `main` ← Compare: `feature/lc-2-listado-stock-completo`
3. Título: `[LC-2] Listado completo de stock en interfaz`
4. Descripción:
   ```
   ## Historia de Usuario LC-2
   Como Administrador quiero poder visualizar el listado de stock disponible 
   en la interfaz, para saber cuántos containers o repuestos tengo disponibles 
   sin tener que consultar directamente la base de datos.
   
   ## Cambios Implementados
   - ✅ Endpoint /stock/listado
   - ✅ Vista con tabs: Ver Listado / Consultar por SKU
   - ✅ Tabla con todo el inventario
   - ✅ Filtros: búsqueda, bodega, bajo stock
   - ✅ KPIs: Total items, Stock total, Bajo stock
   - ✅ Datos de prueba (6 registros)
   ```

---

## Verificación Local

Puedes verificar las ramas localmente:

```powershell
# Ver todas las ramas
git branch -a

# Ver commits de LC-3
git log feature/lc-3-dashboard-tiempo-real --oneline

# Ver commits de LC-2
git log feature/lc-2-listado-stock-completo --oneline

# Ver archivos modificados en LC-3
git diff main..feature/lc-3-dashboard-tiempo-real --name-only

# Ver archivos modificados en LC-2
git diff main..feature/lc-2-listado-stock-completo --name-only
```

---

## Troubleshooting

### Error 403 (sin permisos)
Necesitas que el dueño del repo te agregue como colaborador:
https://github.com/benjita-unab/Software-luxchile/settings/access

### Token inválido
Genera un nuevo token en: https://github.com/settings/tokens

### Conflictos
Si hay conflictos, resuélvelos localmente:
```powershell
git checkout feature/lc-3-dashboard-tiempo-real
git pull origin main
# Resolver conflictos
git add .
git commit -m "Resolver conflictos con main"
git push
```

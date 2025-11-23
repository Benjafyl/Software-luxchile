# Script para detener Docker para LuxChile
# Ejecuta: .\stop-docker.ps1

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "   Deteniendo LuxChile..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Contenedores detenidos correctamente" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR al detener contenedores" -ForegroundColor Red
    exit 1
}

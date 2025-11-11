# start-dev.ps1 — Levanta backend (FastAPI) + frontend (Vite) y abre el navegador.

# Rutas
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackRoot = $RepoRoot
$FrontRoot = Join-Path $RepoRoot 'frontend'

# Asegura .env del frontend apuntando al backend local
$envFile = Join-Path $FrontRoot '.env'
if (-not (Test-Path $envFile)) {
  "VITE_API_BASE=http://127.0.0.1:8000" | Out-File -Encoding utf8 -FilePath $envFile
}

# Comandos a ejecutar en cada ventana
$backendCmd  = "cd `"$BackRoot`"; .\.venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"
$frontendCmd = "cd `"$FrontRoot`"; npm run dev"

# Levanta backend en una nueva ventana de PowerShell
Start-Process -WindowStyle Normal powershell -ArgumentList "-NoExit","-Command",$backendCmd

# Levanta frontend en otra ventana de PowerShell
Start-Process -WindowStyle Normal powershell -ArgumentList "-NoExit","-Command",$frontendCmd

# Abre el navegador después de 2 segundos
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

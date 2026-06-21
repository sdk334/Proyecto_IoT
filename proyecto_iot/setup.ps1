# Setup entorno de desarrollo - Hidroponía IoT
# Ejecutar con: clic derecho -> "Ejecutar con PowerShell"
Set-Location $PSScriptRoot

Write-Host "=== Hidroponía IoT - Setup ===" -ForegroundColor Cyan

# 1. Levantar broker Mosquitto
Write-Host "`n[1/3] Levantando broker MQTT (Mosquitto)..." -ForegroundColor Yellow
docker compose up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: docker compose falló. Asegúrate de que Docker Desktop esté corriendo." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "Broker Mosquitto levantado." -ForegroundColor Green

# 2. Instalar dependencias Python
Write-Host "`n[2/3] Instalando dependencias Python..." -ForegroundColor Yellow
pip install -r bridge\requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip install falló." -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host "Dependencias instaladas." -ForegroundColor Green

# 3. Verificar puerto 1883
Write-Host "`n[3/3] Verificando Mosquitto en puerto 1883..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
$result = Test-NetConnection -ComputerName localhost -Port 1883 -WarningAction SilentlyContinue
if ($result.TcpTestSucceeded) {
    Write-Host "Mosquitto responde en localhost:1883 - OK" -ForegroundColor Green
} else {
    Write-Host "Mosquitto NO responde en puerto 1883. Revisa los logs: docker compose logs mosquitto" -ForegroundColor Red
}

Write-Host "`n=== Setup completado ===" -ForegroundColor Cyan
Write-Host "Proximos pasos:"
Write-Host "  1. Copia bridge\.env.example a bridge\.env y edita tus credenciales Firebase"
Write-Host "  2. Descarga firebase-credentials.json y colócalo en bridge\"
Write-Host "  3. Ejecuta: python bridge\bridge.py"
Read-Host "`nPresiona Enter para salir"

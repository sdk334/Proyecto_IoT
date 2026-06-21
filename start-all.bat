@echo off
echo ========================================
echo  Hidroponía IoT — Iniciando todo
echo ========================================

set "BASE=C:\Users\sdk\Pictures\iot"
set "PROYECTO=%BASE%\proyecto_iot"
set "BRIDGE=%PROYECTO%\bridge"
set "DASHBOARD=%BASE%\hidroponia-dashboard"

echo.
echo [1/3] Levantando Mosquitto (Docker)...
cd /d "%PROYECTO%"
docker compose up -d
timeout /t 3 /nobreak >nul

echo.
echo [2/3] Iniciando bridge MQTT-Firebase...
start "Bridge MQTT-Firebase" cmd /k "cd /d "%BRIDGE%" && python bridge.py"

echo.
echo [3/3] Iniciando dashboard React...
start "Dashboard Hidroponia" cmd /k "cd /d "%DASHBOARD%" && npm run dev"

echo.
echo ========================================
echo  Todo iniciado:
echo    Mosquitto  -> puerto 1883
echo    Bridge     -> ventana "Bridge MQTT-Firebase"
echo    Dashboard  -> http://localhost:5173
echo ========================================
pause

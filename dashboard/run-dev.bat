@echo off
cd /d "%~dp0"
echo ================================
echo  Hidroponia IoT - Dashboard
echo ================================
echo.
echo Instalando dependencias...
call npm install
echo.
echo Iniciando servidor de desarrollo...
echo Abre http://localhost:5173 en tu navegador
echo.
call npm run dev
pause

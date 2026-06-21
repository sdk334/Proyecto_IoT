@echo off
ipconfig | findstr /i "IPv4" > "%~dp0my-ip.txt"
type "%~dp0my-ip.txt"
pause

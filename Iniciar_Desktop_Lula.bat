@echo off
title Desktop Lula
cd /d "%~dp0"

echo ===================================================
echo               DESKTOP LULA (v1.0)
echo ===================================================
echo Iniciando o boneco na area de trabalho...
echo Um icone aparecera perto do relogio (Bandeja do Windows).
echo.

start "" pythonw main.py

if %errorlevel% neq 0 (
    echo [AVISO] Falha ao iniciar com pythonw, tentando com python normal...
    python main.py
)

exit

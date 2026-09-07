@echo off
setlocal
cd /d "%~dp0"

echo === math-validator-2.0 ===
echo Instalacja zaleznosci (fastapi, uvicorn, sympy)...

set "PYCMD=python"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3.14 --version >nul 2>nul
    if not errorlevel 1 (
        set "PYCMD=py -3.14"
    ) else (
        py --version >nul 2>nul
        if not errorlevel 1 set "PYCMD=py"
    )
)

echo Uzywam: %PYCMD%
%PYCMD% -m pip install --quiet fastapi uvicorn sympy
if errorlevel 1 (
    echo.
    echo BLAD: instalacja zaleznosci nie powiodla sie.
    pause
    exit /b 1
)

echo.
echo Uruchamiam API pod http://127.0.0.1:8000
echo (Ctrl+C zeby zatrzymac)
echo.

start "" http://127.0.0.1:8000
%PYCMD% -m uvicorn api:app --reload
if errorlevel 1 (
    echo.
    echo BLAD: serwer zakonczyl sie bledem - tresc bledu powyzej.
)

endlocal
pause

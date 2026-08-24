@echo off
setlocal

echo === math-validator-2.0 ===
echo Instalacja zaleznosci (fastapi, uvicorn, sympy)...

where py >nul 2>nul
if %errorlevel%==0 (
    py -3.14 -m pip install --quiet fastapi uvicorn sympy
    if errorlevel 1 (
        echo Nie udalo sie uzyc "py -3.14", probuje domyslnego "py"...
        py -m pip install --quiet fastapi uvicorn sympy
    )
) else (
    python -m pip install --quiet fastapi uvicorn sympy
)

echo.
echo Uruchamiam API pod http://127.0.0.1:8000
echo (Ctrl+C zeby zatrzymac)
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    py -3.14 -m uvicorn api:app --reload
) else (
    python -m uvicorn api:app --reload
)

endlocal
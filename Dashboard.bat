@echo off

echo Iniciando servidor Django...

REM Ruta absoluta a tu entorno virtual
set VIRTUAL_ENV="C:\Users\diego\OneDrive\Documentos\Repositorios\Lavanderia_aplicacion\.venv\Scripts\activate"

REM Ruta absoluta a tu proyecto Django
set PROJECT_PATH="C:\Users\diego\OneDrive\Documentos\Repositorios\Lavanderia_aplicacion"

REM Activar entorno virtual
call "%VIRTUAL_ENV%"

REM Navegar a la carpeta del proyecto
cd /d "%PROJECT_PATH%"

REM Iniciar el servidor Django en segundo plano
start /b python manage.py runserver

REM Esperar a que el servidor Django esté listo (ajusta el tiempo si es necesario)
timeout /t 5 /nobreak > nul

REM Abrir el navegador en la URL del servidor
start http://127.0.0.1:8000/

echo Servidor Django iniciado y navegador abierto.

pause
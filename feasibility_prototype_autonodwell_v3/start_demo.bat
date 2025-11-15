\
@echo off
cd /d "%~dp0"
set "STREAMLIT_EMAIL="
setx STREAMLIT_SUPPRESS_CONFIG_WARNINGS true >nul
setx STREAMLIT_BROWSER_GUESS false >nul
call venv\Scripts\activate
if not exist logs mkdir logs
start "Autonodwell-Backend" cmd /k "cd /d %~dp0 && python -m uvicorn app.main:app --reload --port 8000 > logs\backend.log 2>&1"
timeout /t 6 /nobreak >nul
start "Autonodwell-UI" cmd /k "cd /d %~dp0\ui && streamlit run streamlit_app.py --server.port 8501 > ..\logs\streamlit.log 2>&1"
timeout /t 8 /nobreak >nul
start http://localhost:8501
echo Autonodwell demo launched. Backend logs: logs\backend.log, UI logs: logs\streamlit.log
pause
exit

@echo off

:: Переход к директории проекта
cd /d C:\project\task

:: Активация виртуального окружения
call venv\Scripts\activate.bat

:: Запуск приложения Streamlit
streamlit run app.py
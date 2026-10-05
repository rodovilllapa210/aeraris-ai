@echo off
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m streamlit run streamlit_app.py
) else (
    python -m streamlit run streamlit_app.py
)

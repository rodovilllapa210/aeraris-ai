#!/usr/bin/env sh
if [ -x ".venv/bin/python" ]; then
    .venv/bin/python -m streamlit run streamlit_app.py
else
    python -m streamlit run streamlit_app.py
fi

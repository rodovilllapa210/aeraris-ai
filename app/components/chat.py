"""Componentes de conversación."""

from __future__ import annotations

import streamlit as st


def render_chat_input() -> str | None:
    """Muestra una entrada de chat todavía no conectada al orquestador."""
    question = st.chat_input("Pregunta algo sobre el análisis")
    if question:
        st.info("Escribe tu consulta en la conversación principal.")
    return question

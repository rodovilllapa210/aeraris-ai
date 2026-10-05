"""Representación visual del trabajo conceptual del agente."""

from __future__ import annotations

import streamlit as st

TECHNICAL_STEP_LABELS = {
    "transaction_analyzer": "Consultando movimientos",
    "financial_calculator": "Comparando con el histórico",
    "financial_explainer": "Preparando una explicación",
    "tool_call": "Procesando información",
    "llm": "Preparando una explicación",
    "calculando métricas con python": "Calculando tus métricas",
    "generando interpretación": "Preparando una explicación",
}


def render_agent_trace(steps: list[str]) -> None:
    """Muestra de forma compacta la actividad comprensible del copiloto."""
    if not steps:
        return

    with st.status("Análisis completado", expanded=False, state="complete"):
        for step in steps:
            st.write(f"✓ {_friendly_step(step)}")


def _friendly_step(step: str) -> str:
    normalized = step.casefold()
    for technical_name, friendly_name in TECHNICAL_STEP_LABELS.items():
        if technical_name in normalized:
            return friendly_name
    return step

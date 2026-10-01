"""Presentación de resultados de análisis."""

from __future__ import annotations

import streamlit as st

from core.schemas import AnalysisResult


def render_analysis_result(result: AnalysisResult) -> None:
    """Muestra el resumen, los datos y las recomendaciones principales."""
    st.write(result.summary)

    data = result.data
    first, second, third = st.columns(3)
    first.metric("Proveedor", data.supplier or "—")
    second.metric("Total", _format_amount(data.total, data.currency))
    third.metric("Vencimiento", data.due_date.isoformat() if data.due_date else "—")

    if result.warnings:
        st.markdown("#### Avisos")
        for warning in result.warnings:
            st.warning(f"{warning.code}: {warning.message}")

    if result.suggested_questions:
        st.markdown("#### Preguntas sugeridas")
        for question in result.suggested_questions:
            st.markdown(f"- {question}")


def _format_amount(value: float | None, currency: str) -> str:
    if value is None:
        return "—"
    return f"{value:,.2f} {currency}".replace(",", "X").replace(".", ",").replace("X", ".")

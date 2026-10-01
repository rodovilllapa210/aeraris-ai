"""Componentes para las futuras visualizaciones."""

from __future__ import annotations

import streamlit as st

from core.schemas import ChartSpec


def render_charts(charts: list[ChartSpec]) -> None:
    """Muestra el estado de las visualizaciones sin dibujar gráficos todavía."""
    if not charts:
        st.caption("No hay visualizaciones disponibles para este análisis.")
        return

    for chart in charts:
        st.write(chart.title)

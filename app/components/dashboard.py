"""Resumen financiero preparado para la futura integración CSV."""

from __future__ import annotations

import streamlit as st

from visualizations.charts import create_expense_category_chart


def render_financial_summary(
    income: float,
    expenses: float,
    savings: float,
    savings_rate: float,
) -> None:
    """Muestra las cuatro métricas principales del resumen financiero."""
    metrics = (
        ("Ingresos", _format_currency(income)),
        ("Gastos", _format_currency(expenses)),
        ("Ahorro", _format_currency(savings)),
        ("Tasa de ahorro", _format_percentage(savings_rate)),
    )
    columns = st.columns(4)
    for index, (label, value) in enumerate(metrics):
        columns[index].metric(label, value)


def render_expense_categories(expenses_by_category: dict[str, float]) -> None:
    """Muestra el gasto por categoría mediante un gráfico Plotly."""
    if not expenses_by_category:
        st.caption("No hay gastos por categoría para representar.")
        return
    figure = create_expense_category_chart(expenses_by_category)
    st.plotly_chart(
        figure,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
    )


def _format_currency(value: float) -> str:
    decimals = 0 if float(value).is_integer() else 2
    return (
        f"{value:,.{decimals}f} €"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def _format_percentage(value: float) -> str:
    return f"{value:.1f} %".replace(".", ",")

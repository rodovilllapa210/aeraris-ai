"""Creación de especificaciones de gráficos."""

from __future__ import annotations

import plotly.graph_objects as go

from core.schemas import ChartSpec, FinancialData


def create_chart_specs(data: FinancialData) -> list[ChartSpec]:
    """Reserva el contrato para los gráficos que se añadirán más adelante."""
    return []


def create_expense_category_chart(
    expenses_by_category: dict[str, float],
) -> go.Figure:
    """Crea un gráfico de barras con los gastos calculados por categoría."""
    categories = list(expenses_by_category)
    values = [expenses_by_category[category] for category in categories]

    figure = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color="#2f6f73",
                hovertemplate="%{x}: %{y:.2f} €<extra></extra>",
            )
        ]
    )
    figure.update_layout(
        title="Gastos por categoría",
        xaxis_title=None,
        yaxis_title="Euros",
        margin=dict(l=20, r=20, t=55, b=20),
        showlegend=False,
    )
    return figure


def create_restaurant_history_chart(
    monthly_spend: dict[str, float],
) -> go.Figure:
    """Crea un gráfico compacto de la evolución de restauración."""
    figure = go.Figure(
        data=[
            go.Bar(
                x=list(monthly_spend),
                y=list(monthly_spend.values()),
                marker_color="#2f6f73",
                text=[f"{value:.0f} €" for value in monthly_spend.values()],
                textposition="outside",
                hovertemplate="%{x}: %{y:.0f} €<extra></extra>",
            )
        ]
    )
    figure.update_layout(
        title="Evolución del gasto en restauración",
        xaxis_title=None,
        yaxis_title="Euros",
        height=280,
        margin=dict(l=20, r=20, t=55, b=20),
        showlegend=False,
    )
    return figure

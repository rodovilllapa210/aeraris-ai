"""Resultados enriquecidos integrados en el flujo conversacional."""

from __future__ import annotations

from datetime import date
from typing import Any

import streamlit as st

from app.components.dashboard import (
    render_expense_categories,
    render_financial_summary,
)
from app.components.research import render_infographic, render_research_result
from visualizations.charts import create_restaurant_history_chart


def render_active_analysis(
    scenario_name: str | None,
    analysis: dict[str, Any],
    csv_analysis: dict[str, Any] | None,
    *,
    autoplay_audio: bool = False,
) -> None:
    """Renderiza el resultado activo dentro de un mensaje del asistente."""
    if scenario_name is None or analysis.get("error"):
        return

    if scenario_name == "research":
        render_research_result(analysis)
        return

    if scenario_name == "infographic":
        render_infographic(analysis.get("image_path", ""))
        return

    if scenario_name == "invoice":
        data = analysis.get("data", {})
        with st.chat_message("assistant"):
            st.markdown(str(analysis.get("summary", "")))
            st.caption("Datos principales")
            _render_key_metrics(
                [
                    ("Consumo", f"{data.get('consumption_kwh', 0)} kWh"),
                    ("Total", _format_currency(data.get("total_eur"))),
                    ("Vencimiento", _format_date(data.get("due_date"))),
                ]
            )
            _render_observations(analysis)
        return

    if scenario_name == "receipt":
        data = analysis.get("data", {})
        with st.chat_message("assistant"):
            st.markdown(str(analysis.get("summary", "")))
            st.caption("Datos principales")
            _render_key_metrics(
                [
                    ("Establecimiento", str(data.get("merchant", "—"))),
                    ("Categoría", str(data.get("category", "—"))),
                    ("Importe", _format_currency(data.get("total_eur"))),
                ]
            )
            _render_observations(analysis)
        return

    if scenario_name == "monthly" and csv_analysis:
        with st.chat_message("assistant"):
            st.markdown(str(analysis.get("summary", "")))
            render_financial_summary(
                income=float(csv_analysis["income"]),
                expenses=float(csv_analysis["expenses"]),
                savings=float(csv_analysis["savings"]),
                savings_rate=float(csv_analysis["savings_rate"]),
            )
            render_expense_categories(
                dict(csv_analysis["expenses_by_category"])
            )
            _render_observations(analysis)
        return

    if scenario_name == "savings":
        results = analysis.get("deterministic_results", {})
        inputs = analysis.get("inputs", {})
        with st.chat_message("assistant"):
            st.caption("Cálculos deterministas realizados con Python")
            st.caption("Tu objetivo de ahorro")
            _render_key_metrics(
                [
                    ("Objetivo", _format_currency(results.get("target_eur"))),
                    (
                        "Disponible",
                        _format_currency(inputs.get("available_savings_eur")),
                    ),
                    ("Pendiente", _format_currency(results.get("remaining_eur"))),
                    (
                        "Tiempo estimado",
                        f"~{results.get('estimated_months', '—')} meses",
                    ),
                ]
            )
            st.markdown(str(analysis.get("model_output", "")))
        return

    if scenario_name in {"receipt_action", "action_response"}:
        with st.chat_message("assistant"):
            st.markdown(str(analysis.get("assistant_response", "")))
            metrics = analysis.get("metrics", [])
            if metrics:
                _render_key_metrics(
                    [
                        (str(item["label"]), str(item["value"]))
                        for item in metrics
                    ]
                )
            chart = analysis.get("chart")
            if isinstance(chart, dict) and chart:
                figure = create_restaurant_history_chart(chart)
                st.plotly_chart(
                    figure,
                    width="stretch",
                    config={"displayModeBar": False, "responsive": True},
                )


def _render_key_metrics(items: list[tuple[str, str]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value) in zip(columns, items):
        column.metric(label, value)


def _render_observations(analysis: dict[str, Any]) -> None:
    observations = analysis.get("observations", [])
    if not observations:
        return
    st.markdown("**Observaciones**")
    for observation in observations:
        st.markdown(f"- {observation}")


def _format_currency(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "—"
    decimals = 0 if float(value).is_integer() else 2
    return (
        f"{float(value):,.{decimals}f} €"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def _format_date(value: Any) -> str:
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError:
        return str(value or "—")
    return parsed.strftime("%d/%m/%Y")

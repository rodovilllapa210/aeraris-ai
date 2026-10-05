"""Pruebas de las continuaciones conversacionales del ticket."""

from __future__ import annotations

from demo.actions import resolve_suggested_action
from demo.loader import load_receipt_analysis


def test_restaurant_comparison_uses_demo_history() -> None:
    result = resolve_suggested_action(
        "Compararlo con otros gastos de restauración",
        "receipt",
    )

    assert result is not None
    response = result["assistant_response"]
    assert response != load_receipt_analysis()["summary"]
    assert "168 €" in response
    assert "196 €" in response
    assert "214 €" in response
    assert result["chart"] == {
        "Julio": 168.0,
        "Agosto": 196.0,
        "Septiembre": 214.0,
    }
    assert result["suggested_actions"] == [
        "Comparar restauración con ocio",
        "Ver cuánto ha aumentado",
        "Simular impacto sobre mi ahorro",
    ]


def test_receipt_category_total_uses_september_total() -> None:
    result = resolve_suggested_action(
        "Ver cuánto llevo gastado en esta categoría",
        "receipt",
    )

    assert result is not None
    assert "214 €" in result["assistant_response"]
    assert "22,3 %" in result["assistant_response"]


def test_add_receipt_to_monthly_analysis_has_new_actions() -> None:
    result = resolve_suggested_action(
        "Incorporar el gasto al análisis mensual",
        "receipt",
    )

    assert result is not None
    assert "47,80 €" in result["assistant_response"]
    assert "214 €" in result["assistant_response"]
    assert result["suggested_actions"] == [
        "Ver cuánto representa sobre el gasto mensual",
        "Comparar restauración con otros meses",
        "Explorar mi ahorro del mes",
    ]


def test_receipt_actions_are_not_applied_to_other_scenarios() -> None:
    result = resolve_suggested_action(
        "Compararlo con otros gastos de restauración",
        "monthly",
    )

    assert result is None

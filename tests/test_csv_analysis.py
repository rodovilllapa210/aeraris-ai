"""Pruebas de los cálculos deterministas sobre movimientos."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.schemas import AnalysisStatus
from processors.csv import analyze_transactions, process_csv

CSV_PATH = Path("demo_data/transactions/movimientos_septiembre.csv")


def test_september_financial_metrics_are_calculated_from_csv() -> None:
    result = analyze_transactions(CSV_PATH)

    assert result.income == 2450.0
    assert result.expenses == 1780.0
    assert result.savings == 670.0
    assert result.savings_rate == pytest.approx(27.3, abs=0.1)


def test_expenses_are_grouped_by_category() -> None:
    result = analyze_transactions(CSV_PATH)

    assert "Ingresos" not in result.expenses_by_category
    assert result.expenses_by_category["Restauracion"] == 214.0
    assert sum(result.expenses_by_category.values()) == pytest.approx(1780.0)


def test_process_csv_populates_common_contract() -> None:
    result = process_csv(str(CSV_PATH))

    assert result.status == AnalysisStatus.SUCCESS
    assert result.data.total_income == 2450.0
    assert result.data.total_expenses == 1780.0
    assert result.data.net_cash_flow == 670.0
    assert result.data.extra["savings_rate"] == pytest.approx(27.3)

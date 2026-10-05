"""Análisis determinista de movimientos financieros en CSV."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, Field

from core.schemas import (
    AnalysisResult,
    AnalysisStatus,
    FinancialData,
    InputType,
)


class TransactionAnalysis(BaseModel):
    """Métricas calculadas directamente desde los movimientos."""

    income: float
    expenses: float
    savings: float
    savings_rate: float
    expenses_by_category: dict[str, float] = Field(default_factory=dict)


def analyze_transactions(source: Any) -> TransactionAnalysis:
    """Calcula ingresos, gastos, ahorro y categorías desde un CSV."""
    if hasattr(source, "seek"):
        source.seek(0)

    frame = pd.read_csv(source, encoding="utf-8-sig")
    required_columns = {"categoria", "importe_eur"}
    missing = required_columns.difference(frame.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Faltan columnas obligatorias: {missing_text}")

    amounts = pd.to_numeric(frame["importe_eur"], errors="raise")
    income = round(float(amounts[amounts > 0].sum()), 2)
    expenses = round(float(-amounts[amounts < 0].sum()), 2)
    savings = round(income - expenses, 2)
    savings_rate = round((savings / income * 100) if income else 0.0, 1)

    expense_rows = pd.DataFrame(
        {
            "category": (
                frame.loc[amounts < 0, "categoria"]
                .fillna("Sin categoría")
                .astype(str)
                .str.strip()
            ),
            "expense": -amounts[amounts < 0],
        }
    )
    expense_rows = expense_rows[
        expense_rows["category"].str.casefold() != "ingresos"
    ]
    grouped = expense_rows.groupby("category", sort=False)["expense"].sum()
    expenses_by_category = {
        str(category): round(float(value), 2)
        for category, value in grouped.items()
    }

    return TransactionAnalysis(
        income=income,
        expenses=expenses,
        savings=savings,
        savings_rate=savings_rate,
        expenses_by_category=expenses_by_category,
    )


def process_csv(file_path: str) -> AnalysisResult:
    """Procesa un CSV real conservando el contrato común del orquestador."""
    try:
        analysis = analyze_transactions(file_path)
    except Exception as exc:
        return AnalysisResult(
            input_type=InputType.CSV,
            source_name=Path(file_path).name,
            status=AnalysisStatus.ERROR,
            errors=[f"No se pudo analizar el CSV: {exc}"],
        )

    return AnalysisResult(
        input_type=InputType.CSV,
        source_name=Path(file_path).name,
        status=AnalysisStatus.SUCCESS,
        data=FinancialData(
            document_type="transaction_csv",
            total_income=analysis.income,
            total_expenses=analysis.expenses,
            net_cash_flow=analysis.savings,
            categories=analysis.expenses_by_category,
            extra={"savings_rate": analysis.savings_rate},
        ),
        summary=(
            f"Ingresos: {analysis.income:.2f} EUR; "
            f"gastos: {analysis.expenses:.2f} EUR; "
            f"ahorro: {analysis.savings:.2f} EUR."
        ),
    )

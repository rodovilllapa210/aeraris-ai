"""Reglas deterministas aplicadas a los datos financieros."""

from __future__ import annotations

from core.schemas import AnalysisWarning, FinancialData


def evaluate_financial_rules(data: FinancialData) -> list[AnalysisWarning]:
    """Evalúa las reglas financieras deterministas que se añadirán más adelante."""
    return []

"""Pruebas mínimas de los contratos compartidos."""

from __future__ import annotations

from core.schemas import AnalysisResult, FinancialData, InputType


def test_create_financial_data() -> None:
    data = FinancialData(supplier="ACME SL", total=1210.0)

    assert data.supplier == "ACME SL"
    assert data.total == 1210.0
    assert data.currency == "EUR"
    assert data.categories == {}


def test_create_analysis_result() -> None:
    result = AnalysisResult(input_type=InputType.TEXT, summary="Análisis correcto")

    assert result.input_type == InputType.TEXT
    assert result.summary == "Análisis correcto"
    assert result.data == FinancialData()


def test_model_dump_serialization() -> None:
    result = AnalysisResult(
        input_type=InputType.PDF,
        data=FinancialData(total=99.5),
    )

    payload = result.model_dump(mode="json")

    assert payload["input_type"] == "pdf"
    assert payload["data"]["total"] == 99.5
    assert payload["warnings"] == []

"""Pruebas del cargador de outputs reales de demostración."""

from __future__ import annotations

import pytest

from demo.loader import (
    detect_scenario,
    load_invoice_analysis,
    load_monthly_analysis,
    load_receipt_analysis,
    load_savings_plan,
    load_scenario,
    load_voice_analysis,
)


def test_load_document_and_monthly_outputs() -> None:
    invoice = load_invoice_analysis()
    receipt = load_receipt_analysis()
    monthly = load_monthly_analysis()

    assert invoice["data"]["consumption_kwh"] == 267
    assert invoice["data"]["total_eur"] == 91.24
    assert receipt["data"]["merchant"] == "La Terraza"
    assert receipt["data"]["total_eur"] == 47.8
    assert monthly["deterministic_data"]["savings_eur"] == 670.0


def test_load_voice_and_savings_outputs() -> None:
    voice = load_voice_analysis()
    savings = load_savings_plan()

    assert (
        voice["speech_to_text"]["transcription"]
        == "¿Estoy gastando demasiado en restaurantes?"
    )
    assert voice["model_output"]
    assert savings["deterministic_results"] == {
        "target_eur": 5062.0,
        "remaining_eur": 3062.0,
        "estimated_months": 5,
    }


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("factura_electricidad_septiembre.pdf", "invoice"),
        ("ticket_restaurante.png", "receipt"),
        ("ticket_restaurante.pdf", "receipt"),
        ("movimientos_septiembre.csv", "monthly"),
        ("FACTURA_ELECTRICIDAD_SEPTIEMBRE.PDF", "invoice"),
    ],
)
def test_detect_scenario(filename: str, expected: str) -> None:
    assert detect_scenario(filename) == expected


def test_unknown_file_has_no_scenario() -> None:
    assert detect_scenario("extracto_enero.csv") is None


def test_missing_json_returns_controlled_error() -> None:
    result = load_scenario("missing.json")

    assert "error" in result
    assert result["suggested_actions"] == []


def test_loader_rejects_paths_outside_outputs() -> None:
    result = load_scenario("../invoice_analysis.json")

    assert "error" in result

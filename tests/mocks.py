"""Objetos simulados reutilizables en pruebas y demostraciones."""

from __future__ import annotations

from datetime import date

from core.schemas import (
    AnalysisResult,
    AnalysisWarning,
    FinancialData,
    InputType,
    WarningLevel,
)


def mock_invoice_result() -> AnalysisResult:
    """Crea el resultado de la factura utilizado por el modo demostración."""
    return AnalysisResult(
        input_type=InputType.PDF,
        source_name="factura_demo.pdf",
        data=FinancialData(
            document_type="invoice",
            supplier="ACME SL",
            document_number="2026-001",
            date=date(2026, 9, 30),
            due_date=date(2026, 10, 14),
            subtotal=1000.00,
            tax=210.00,
            total=1210.00,
            currency="EUR",
        ),
        summary=(
            "Factura de ACME SL por un importe total de 1.210 €, "
            "con vencimiento el 14 de octubre."
        ),
        warnings=[
            AnalysisWarning(
                level=WarningLevel.WARNING,
                code="PAYMENT_DUE_SOON",
                message="El pago vence próximamente.",
            )
        ],
        suggested_questions=[
            "¿Cuánto IVA incluye?",
            "¿Cuándo vence?",
            "¿Cuál es el importe antes de impuestos?",
        ],
    )

"""Respuestas simuladas del futuro modelo de lenguaje."""

from __future__ import annotations

from core.schemas import FinancialData


def generate_summary(
    data: FinancialData,
    extracted_text: str | None = None,
) -> str:
    """Genera un resumen simulado sin invocar ningún modelo externo."""
    source = " con texto extraído" if extracted_text else ""
    return f"[MOCK] Resumen financiero provisional{source}."


def suggest_questions(data: FinancialData) -> list[str]:
    """Devuelve preguntas simuladas para validar el contrato de integración."""
    return [
        "[MOCK] ¿Cuál es el dato financiero más relevante?",
        "[MOCK] ¿Hay algún vencimiento próximo?",
    ]


def answer_question(question: str, context: str) -> str:
    """Devuelve una respuesta simulada sin conectarse a Ollama."""
    return f"[MOCK] Respuesta provisional a: {question}"

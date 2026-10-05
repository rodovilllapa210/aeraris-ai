"""Contratos del recorrido narrativo de la demo de Aeraris."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DemoStage(str, Enum):
    """Estados visibles del recorrido principal de la presentación."""

    START = "start"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    NEED_TRANSACTIONS = "need_transactions"
    MONTHLY_ANALYSIS = "monthly_analysis"
    VOICE_ANALYSIS = "voice_analysis"
    SAVINGS_BRIDGE = "savings_bridge"
    SAVINGS_PLAN = "savings_plan"
    SUMMARY_AUDIO = "summary_audio"
    OPEN_CHAT = "open_chat"
    WEB_RESEARCH = "web_research"
    RESEARCH_RESULT = "research_result"
    INFOGRAPHIC_GENERATION = "infographic_generation"
    INFOGRAPHIC = "infographic"


@dataclass(frozen=True)
class DemoDocument:
    """Documento preparado que puede activarse desde el contexto."""

    label: str
    filename: str


AVAILABLE_DOCUMENTS = (
    DemoDocument(
        "Factura electricidad — septiembre",
        "factura_electricidad_septiembre.pdf",
    ),
    DemoDocument("Ticket restaurante", "ticket_restaurante.pdf"),
    DemoDocument("Movimientos — septiembre", "movimientos_septiembre.csv"),
)

INVOICE_ACTIONS = [
    "Entender los principales conceptos",
    "Compararlo con información anterior",
    "Ver su impacto en mis gastos",
]

NEED_TRANSACTIONS_ACTIONS = [
    "Analizar movimientos",
    "Ahora no",
]

MONTHLY_ACTIONS = [
    "Ver qué gastos han aumentado",
    "Preguntar por voz",
    "Explorar un objetivo de ahorro",
]

VOICE_ACTIONS = [
    "Ver evolución",
    "Comparar con otras categorías",
    "Simular impacto sobre mi ahorro",
]

SAVINGS_BRIDGE_ACTIONS = [
    "Explorar objetivo de ahorro",
    "Volver al análisis mensual",
]

SAVINGS_PLAN_ACTIONS = [
    "Simular otro objetivo",
    "Cambiar ahorro mensual",
    "Escuchar resumen",
]


DOCUMENT_LABELS = {item.filename: item.label for item in AVAILABLE_DOCUMENTS}


def document_label(filename: str) -> str:
    """Devuelve el nombre de presentación de un archivo de demo."""
    return DOCUMENT_LABELS.get(filename, filename)


def stage_for_scenario(scenario_name: str | None) -> DemoStage:
    """Mapea un escenario cargado al estado narrativo correspondiente."""
    return {
        "invoice": DemoStage.INVOICE,
        "receipt": DemoStage.RECEIPT,
        "monthly": DemoStage.MONTHLY_ANALYSIS,
        "voice_restaurant": DemoStage.VOICE_ANALYSIS,
        "savings": DemoStage.SAVINGS_PLAN,
    }.get(scenario_name, DemoStage.START)

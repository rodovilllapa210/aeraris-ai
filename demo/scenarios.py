"""Datos MOCK temporales para los flujos de demostración."""

from __future__ import annotations

from typing import Any

SCENARIOS: dict[str, dict[str, Any]] = {
    "invoice": {
        "summary": (
            "La factura asciende a 86,42 € y su vencimiento está previsto "
            "para el 15 de octubre."
        ),
        "suggested_actions": [
            "Entender los principales conceptos",
            "Compararlo con información anterior",
            "Revisar la fecha de vencimiento",
        ],
    },
    "receipt": {
        "summary": (
            "El ticket corresponde a un gasto de restauración de 42,60 €. "
            "Todavía no se ha incorporado al histórico."
        ),
        "suggested_actions": [
            "Clasificar este gasto",
            "Ver su impacto en mis gastos",
            "Compararlo con otros restaurantes",
        ],
    },
    "voice_restaurant": {
        "user_message": "¿Estoy gastando demasiado en restaurantes?",
        "summary": (
            "Este mes has gastado 214 € en restauración, frente a una media "
            "de 182 € durante los dos meses anteriores."
        ),
        "trace_steps": [
            "Entendiendo la pregunta",
            "Consultando movimientos del mes",
            "Comparando con histórico",
        ],
        "suggested_actions": [
            "Ver los gastos por restaurante",
            "Comparar los últimos tres meses",
            "Definir un objetivo mensual",
        ],
    },
    "savings": {
        "summary": (
            "Este mes mantienes una tasa de ahorro del 23,3 %. "
            "Los datos son simulados para esta demostración."
        ),
        "metrics": {
            "income": 3000.0,
            "expenses": 2300.0,
            "savings": 700.0,
            "savings_rate": 23.3,
        },
        "suggested_actions": [
            "Entender los principales conceptos",
            "Compararlo con información anterior",
            "Ver su impacto en mis gastos",
        ],
    },
}

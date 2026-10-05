"""Continuaciones conversacionales deterministas para la demostración."""

from __future__ import annotations

from typing import Any

RESTAURANT_SPEND_EUR = {
    "Julio": 168.0,
    "Agosto": 196.0,
    "Septiembre": 214.0,
}
RECEIPT_AMOUNT_EUR = 47.80


def resolve_suggested_action(
    action: str,
    current_scenario: str | None,
) -> dict[str, Any] | None:
    """Devuelve una continuación del ticket cuando la acción es conocida."""
    if current_scenario != "receipt":
        return None

    handlers = {
        "Incorporar el gasto al análisis mensual": _add_to_monthly_analysis,
        "Compararlo con otros gastos de restauración": _compare_restaurant_spend,
        "Ver cuánto llevo gastado en esta categoría": _show_category_total,
    }
    handler = handlers.get(action)
    return handler() if handler else None


def _add_to_monthly_analysis() -> dict[str, Any]:
    return _result(
        response=(
            "El gasto de 47,80 € se incorpora a la categoría Restauración "
            "del análisis de septiembre. El total mensual de esta categoría "
            "es de 214 €."
        ),
        suggested_actions=[
            "Ver cuánto representa sobre el gasto mensual",
            "Comparar restauración con otros meses",
            "Explorar mi ahorro del mes",
        ],
    )


def _compare_restaurant_spend() -> dict[str, Any]:
    return _result(
        response=(
            "Este gasto de 47,80 € representa alrededor del 22 % de los "
            "214 € gastados en restauración durante septiembre.\n\n"
            "El gasto mensual en restauración ha evolucionado desde 168 € "
            "en julio y 196 € en agosto hasta 214 € en septiembre."
        ),
        suggested_actions=[
            "Comparar restauración con ocio",
            "Ver cuánto ha aumentado",
            "Simular impacto sobre mi ahorro",
        ],
        chart=RESTAURANT_SPEND_EUR,
    )


def _show_category_total() -> dict[str, Any]:
    percentage = RECEIPT_AMOUNT_EUR / RESTAURANT_SPEND_EUR["Septiembre"] * 100
    percentage_text = f"{percentage:.1f}".replace(".", ",")
    return _result(
        response=(
            "En septiembre llevas 214 € gastados en restauración. "
            f"Este ticket de 47,80 € supone aproximadamente el "
            f"{percentage_text} % del total de la categoría."
        ),
        suggested_actions=[
            "Comparar con meses anteriores",
            "Ver otros gastos discrecionales",
            "Simular impacto sobre mi ahorro",
        ],
    )


def _result(
    response: str,
    suggested_actions: list[str],
    chart: dict[str, float] | None = None,
) -> dict[str, Any]:
    return {
        "assistant_response": response,
        "metrics": [],
        "chart": chart,
        "suggested_actions": suggested_actions,
    }

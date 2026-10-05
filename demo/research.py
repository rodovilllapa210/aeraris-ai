"""Respuesta educativa precalculada para la continuación conversacional."""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path
from typing import Any

RESEARCH_PATH = (
    Path(__file__).resolve().parents[1]
    / "demo_data"
    / "outputs"
    / "compound_interest_research.json"
)

RESEARCH_STEPS = [
    "✓ Analizando la consulta",
    "✓ Buscando información fiable en la web",
    "✓ Contrastando fuentes",
    "✓ Preparando una explicación sencilla",
]


def load_compound_interest_research() -> dict[str, Any]:
    """Carga la respuesta educativa generada previamente."""
    with RESEARCH_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def is_compound_interest_query(text: str) -> bool:
    """Reconoce la intención sin exigir una frase exacta."""
    normalized = _normalize(text)
    return "interes compuesto" in normalized


def build_research_markdown(
    research: dict[str, Any],
    *,
    include_offer: bool = True,
) -> str:
    """Convierte el JSON educativo en una respuesta conversacional compacta."""
    sections = research.get("sections", {})
    example = sections.get("ejemplo", {})
    lines = [
        "### INTERÉS COMPUESTO",
        "",
        str(sections.get("definicion", "")),
        "",
        "**Cómo funciona**",
        str(sections.get("como_funciona", "")),
        "",
        "**Fórmula**",
        f"`{sections.get('formula', '')}`",
        "",
        "**Ejemplo**",
        (
            f"**{_currency(example.get('capital_inicial_eur'))}** · "
            f"**{_number(example.get('tipo_anual_pct'))} % anual** · "
            f"**{example.get('anos', '—')} años**"
        ),
        (
            f"→ Valor final con interés compuesto: "
            f"**{_currency(example.get('valor_final_compuesto_eur'))}**"
        ),
        (
            f"Con interés simple: **{_currency(example.get('valor_final_simple_eur'))}**."
        ),
        "",
        "**Interés simple vs. compuesto**",
        str(sections.get("interes_simple_vs_compuesto", "")),
        "",
        "**Por qué importa el tiempo**",
        str(sections.get("por_que_importa_el_tiempo", "")),
        "",
        "**Conclusión**",
        str(sections.get("conclusion_educativa", "")),
        "",
        "**Fuentes consultadas**",
    ]
    for source in research.get("sources", []):
        title = source.get("title", "Fuente")
        url = source.get("url", "")
        supports = source.get("supports", "")
        lines.append(f"- [{title}]({url}) — {supports}")

    if include_offer:
        lines.extend(
            [
                "",
                "Si quieres, también puedo crear una infografía, mostrarte "
                "el ejemplo paso a paso o comparar el interés simple con el compuesto.",
            ]
        )
    return "\n".join(lines)


def build_execution_trace() -> str:
    """Devuelve el informe compacto que permanece en el historial."""
    return "🔎 Investigando\n\n" + "\n".join(RESEARCH_STEPS)


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.casefold())
    return "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
    )


def _number(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):g}"
    return "—"


def _currency(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return "—"
    return (
        f"{float(value):,.2f} €"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

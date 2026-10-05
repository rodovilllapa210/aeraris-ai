"""Asset preparado para la continuación visual de la demo."""

from __future__ import annotations

import unicodedata
from pathlib import Path

INFOGRAPHIC_PATH = (
    Path(__file__).resolve().parents[1]
    / "demo_data"
    / "images"
    / "compound_interest_infographic.png"
)

INFOGRAPHIC_STEPS = [
    "✓ Seleccionando las ideas principales",
    "✓ Preparando la composición visual",
    "✓ Generando la infografía",
]


def is_infographic_confirmation(text: str) -> bool:
    """Reconoce una confirmación solo en el contexto de la propuesta."""
    normalized = _normalize(text).strip()
    if "infograf" in normalized:
        return any(
            phrase in normalized
            for phrase in (
                "hazla",
                "haz la",
                "crea",
                "crear",
                "quiero",
                "si",
            )
        )
    return normalized in {"si", "sí", "si, hazla", "sí, hazla"}


def build_execution_trace() -> str:
    """Devuelve el informe compacto que permanece en el historial."""
    return "🎨 Creando infografía\n\n" + "\n".join(INFOGRAPHIC_STEPS)


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.casefold())
    return "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
    )

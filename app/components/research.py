"""Renderizado conversacional de la investigación y la infografía."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import streamlit as st

from demo.infographic import INFOGRAPHIC_STEPS
from demo.research import RESEARCH_STEPS, build_research_markdown


def render_research_progress() -> None:
    """Simula brevemente el trabajo de investigación y conserva la secuencia visual."""
    with st.status("🔎 Investigando", expanded=True) as status:
        for step in RESEARCH_STEPS:
            st.write(step)
            time.sleep(0.45)
        status.update(
            label="Investigación completada",
            state="complete",
            expanded=False,
        )


def render_infographic_progress() -> None:
    """Simula brevemente la preparación de la infografía."""
    with st.status("🎨 Creando infografía", expanded=True) as status:
        for step in INFOGRAPHIC_STEPS:
            st.write(step)
            time.sleep(0.45)
        status.update(
            label="Infografía preparada",
            state="complete",
            expanded=False,
        )


def render_research_result(research: dict[str, Any]) -> None:
    """Muestra la explicación y sus fuentes dentro de la conversación."""
    with st.chat_message("assistant"):
        st.markdown(build_research_markdown(research))


def render_infographic(image_path: str | Path) -> None:
    """Integra la imagen preparada en una respuesta de Aeraris."""
    with st.chat_message("assistant"):
        st.markdown("He preparado una versión visual sencilla del ejemplo.")
        path = Path(image_path)
        if path.is_file():
            st.image(str(path), use_container_width=True)
        else:
            st.caption("La infografía no está disponible en este momento.")

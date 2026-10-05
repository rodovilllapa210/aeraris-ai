"""Panel con el contexto temporal de la sesión."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from demo.flow import AVAILABLE_DOCUMENTS, document_label


def render_context_panel(items: list[str] | None = None) -> str | None:
    """Muestra un resumen compacto y una biblioteca desplegable."""
    st.markdown("**CONTEXTO ACTUAL**")
    current_items = (
        items
        if items is not None
        else list(st.session_state.get("context_items", []))
    )

    selected_document: str | None = None
    active_items = set(current_items)
    if current_items:
        count = len(current_items)
        suffix = "documento activo" if count == 1 else "documentos activos"
        st.caption(f"{count} {suffix}")
    else:
        st.caption("Ningún documento activo.")

    with st.expander("Biblioteca de documentos", expanded=False):
        if current_items:
            st.caption("Activos")
            for item in current_items:
                st.caption(f"{_icon_for(item)} {document_label(item)}")

        st.caption("Disponibles")
        for document in AVAILABLE_DOCUMENTS:
            if document.filename in active_items:
                continue
            if st.button(
                document.label,
                key=f"demo_document_{document.filename}",
                use_container_width=True,
            ):
                selected_document = document.filename
    return selected_document


def _icon_for(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        return "📄"
    if suffix == ".csv":
        return "📊"
    if suffix in {".png", ".jpg", ".jpeg"}:
        return "🖼"
    return "•"

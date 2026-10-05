"""Acciones contextuales para continuar una conversación."""

from __future__ import annotations

import streamlit as st


def render_suggested_actions(actions: list[str]) -> str | None:
    """Muestra hasta tres acciones y devuelve la seleccionada."""
    visible_actions = actions[:3]
    if not visible_actions:
        return None

    selected_action: str | None = None

    st.caption("Puedes seguir con:")
    columns = st.columns(len(visible_actions))
    for index, action in enumerate(visible_actions):
        if columns[index].button(
            action,
            key=f"suggested_action_{index}",
            type="secondary",
        ):
            selected_action = action

    return selected_action

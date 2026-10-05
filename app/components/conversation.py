"""Mensajes de la conversación mantenidos en la sesión."""

from __future__ import annotations

from typing import Literal

import streamlit as st

INITIAL_ASSISTANT_MESSAGE = (
    "Hola. Puedo ayudarte a entender documentos, gastos y conceptos financieros. "
    "Puedes escribir, hablar o adjuntar información."
)

MessageRole = Literal["user", "assistant"]


def add_message(role: MessageRole, content: str) -> None:
    """Añade un mensaje válido al historial temporal."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
        ]
    st.session_state.messages.append({"role": role, "content": content})


def render_conversation(
    messages: list[dict[str, str]] | None = None,
) -> None:
    """Renderiza el historial mediante los componentes de chat de Streamlit."""
    current_messages = (
        messages
        if messages is not None
        else list(st.session_state.get("messages", []))
    )
    for message in current_messages:
        role = message.get("role")
        content = message.get("content", "")
        if role not in {"user", "assistant"}:
            continue
        with st.chat_message(role):
            st.markdown(content)

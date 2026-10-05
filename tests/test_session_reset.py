"""Pruebas del reinicio selectivo de la conversación."""

from __future__ import annotations

from typing import Any

import app.session as session
from app.components.conversation import INITIAL_ASSISTANT_MESSAGE
from demo.flow import DemoStage


def _populated_state() -> dict[str, Any]:
    return {
        "messages": [
            {"role": "user", "content": "Analiza mis movimientos"},
            {"role": "assistant", "content": "Aquí tienes el resumen"},
        ],
        "context_items": ["movimientos_septiembre.csv"],
        "processed_uploads": ["movimientos_septiembre.csv"],
        "active_scenario": "monthly",
        "active_analysis": {"suggested_actions": ["Crear objetivo de ahorro"]},
        "csv_analysis": {"income": 2450.0, "expenses": 1780.0},
        "agent_trace": ["Analizando movimientos"],
        "active_suggested_actions": [
            "Ver categorías",
            "Explorar un objetivo de ahorro",
        ],
        "upload_widget_version": 4,
        "conversation_attachment_4": object(),
        "voice_action": True,
        "suggested_action_0": True,
        "suggested_action_1": False,
        "suggested_action_2": False,
        "app_configuration": {"locale": "es"},
    }


def test_reset_session_clears_conversation_and_context(monkeypatch) -> None:
    state = _populated_state()
    monkeypatch.setattr(session.st, "session_state", state)

    session.reset_session()

    assert state["messages"] == [
        {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
    ]
    assert state["context_items"] == []
    assert state["processed_uploads"] == []
    assert state["active_scenario"] is None
    assert state["active_analysis"] == {}
    assert state["csv_analysis"] is None
    assert state["agent_trace"] == []
    assert state["active_suggested_actions"] == []
    assert state["demo_stage"] == DemoStage.START.value
    assert state["voice_prompt_pending"] is False
    assert state["upload_widget_version"] == 5
    assert "conversation_attachment_4" not in state


def test_reset_session_clears_widgets_but_preserves_global_state(
    monkeypatch,
) -> None:
    state = _populated_state()
    monkeypatch.setattr(session.st, "session_state", state)

    session.reset_session()
    session.reset_session()

    assert state["app_configuration"] == {"locale": "es"}
    assert state["upload_widget_version"] == 6
    for key in session.TRANSIENT_WIDGET_KEYS:
        assert key not in state


def test_current_upload_widget_key_uses_session_version(monkeypatch) -> None:
    state = {"upload_widget_version": 7}
    monkeypatch.setattr(session.st, "session_state", state)

    assert session.current_upload_widget_key() == "conversation_attachment_7"

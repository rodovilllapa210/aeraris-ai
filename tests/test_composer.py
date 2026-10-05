"""Pruebas del envío unificado de texto, archivos y voz."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import app.session as session
from app.components.conversation import INITIAL_ASSISTANT_MESSAGE


class SessionState(dict[str, Any]):
    """Contenedor mínimo con la semántica de atributo de SessionState."""

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


class NamedUpload(BytesIO):
    def __init__(self, name: str, content: bytes) -> None:
        super().__init__(content)
        self.name = name


def _state() -> SessionState:
    state = SessionState(
        messages=[
            {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
        ]
    )
    state.update(session._fresh_session_defaults())
    return state


def test_composer_file_and_text_share_one_submission(monkeypatch) -> None:
    state = _state()
    monkeypatch.setattr(session.st, "session_state", state)
    csv_path = Path("demo_data/transactions/movimientos_septiembre.csv")
    upload = NamedUpload(csv_path.name, csv_path.read_bytes())
    submission = SimpleNamespace(
        text="Analiza estos movimientos",
        files=[upload],
        audio=None,
    )

    session.handle_composer_submission(submission)

    assert state["active_scenario"] == "monthly"
    assert state["context_items"] == [csv_path.name]
    assert state["messages"][1] == {
        "role": "user",
        "content": "Analiza estos movimientos",
    }
    assert state["csv_analysis"]["savings"] == 670.0
    assert len(state["active_suggested_actions"]) == 3


def test_composer_audio_uses_existing_voice_scenario(monkeypatch) -> None:
    state = _state()
    monkeypatch.setattr(session.st, "session_state", state)
    monkeypatch.setattr(session.st, "toast", lambda *_args, **_kwargs: None)

    session.handle_composer_submission(
        SimpleNamespace(text="", files=[], audio=object())
    )

    assert state["active_scenario"] == "voice_restaurant"
    assert state["messages"][1]["role"] == "user"
    assert state["messages"][1]["content"] == (
        "¿Estoy gastando demasiado en restaurantes?"
    )


def test_composer_text_keeps_chat_input_available(monkeypatch) -> None:
    state = _state()
    monkeypatch.setattr(session.st, "session_state", state)

    session.handle_composer_submission(
        SimpleNamespace(text="¿Qué significa este gasto?", files=[], audio=None)
    )

    assert state["messages"][1] == {
        "role": "user",
        "content": "¿Qué significa este gasto?",
    }

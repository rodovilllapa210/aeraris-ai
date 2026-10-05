"""Pruebas del recorrido educativo de Prompt9."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.components.conversation import INITIAL_ASSISTANT_MESSAGE
from demo.flow import DemoStage
from demo.infographic import INFOGRAPHIC_PATH
from demo.research import load_compound_interest_research

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _app() -> AppTest:
    return AppTest.from_file(
        str(PROJECT_ROOT / "streamlit_app.py"),
        default_timeout=10,
    ).run()


def _at_summary_audio(app: AppTest) -> None:
    app.session_state["context_items"] = ["movimientos_septiembre.csv"]
    app.session_state["processed_uploads"] = ["movimientos_septiembre.csv"]
    app.session_state["active_scenario"] = "summary_audio"
    app.session_state["active_analysis"] = {"suggested_actions": []}
    app.session_state["active_suggested_actions"] = []
    app.session_state["demo_stage"] = DemoStage.SUMMARY_AUDIO.value
    app.run()


def _submit_text(app: AppTest, text: str) -> None:
    app.chat_input[0].set_value(text).run()


def test_compound_interest_research_is_contextual_and_uses_three_sources() -> None:
    app = _app()
    _at_summary_audio(app)

    _submit_text(app, "Explícame el interés compuesto")

    assert not app.exception
    assert app.session_state["demo_stage"] == DemoStage.RESEARCH_RESULT.value
    assert app.session_state["active_scenario"] == "research"
    assert app.session_state["research_offer_active"] is True
    assert app.session_state["active_suggested_actions"] == []
    assert "Explícame el interés compuesto" in [
        message["content"]
        for message in app.session_state["messages"]
    ]

    markdown_text = "\n".join(item.value for item in app.markdown)
    assert "1.000,00 €" in markdown_text
    assert "5 % anual" in markdown_text
    assert "10 años" in markdown_text
    assert "1.628,89 €" in markdown_text
    assert "1.500,00 €" in markdown_text
    research = load_compound_interest_research()
    assert markdown_text.count("https://") == len(research["sources"]) == 3
    assert "🔎 Investigando" in markdown_text
    assert all(
        not button.label.startswith("Crear una infografía")
        for button in app.button
    )


def test_affirmative_confirmation_creates_infographic_only_after_offer() -> None:
    app = _app()
    _at_summary_audio(app)
    _submit_text(app, "¿Qué es el interés compuesto?")

    _submit_text(app, "Sí")

    assert not app.exception
    assert app.session_state["demo_stage"] == DemoStage.INFOGRAPHIC.value
    assert app.session_state["active_scenario"] == "infographic"
    assert app.session_state["research_offer_active"] is False
    assert app.session_state["active_suggested_actions"] == []
    assert INFOGRAPHIC_PATH.is_file()
    assert len(app.get("image")) == 1
    markdown_text = "\n".join(item.value for item in app.markdown)
    assert "🎨 Creando infografía" in markdown_text


def test_affirmative_text_without_research_offer_does_not_create_infographic() -> None:
    app = _app()

    _submit_text(app, "Sí")

    assert not app.exception
    assert app.session_state["demo_stage"] == DemoStage.START.value
    assert app.session_state["active_scenario"] is None
    assert len(app.get("image")) == 0
    assert app.session_state["messages"][-1] == {
        "role": "assistant",
        "content": (
            "Adjunta un documento o movimientos para contextualizar la "
            "conversación."
        ),
    }


def test_reset_clears_prompt9_state() -> None:
    app = _app()
    _at_summary_audio(app)
    _submit_text(app, "Explícame interés compuesto")
    assert app.session_state["research_offer_active"] is True

    next(button for button in app.button if button.label == "Nueva conversación").click().run()

    assert not app.exception
    assert app.session_state["demo_stage"] == DemoStage.START.value
    assert app.session_state["research_offer_active"] is False
    assert app.session_state["active_scenario"] is None
    assert app.session_state["messages"] == [
        {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
    ]

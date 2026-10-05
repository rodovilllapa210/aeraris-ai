"""Pruebas del recorrido determinista de la demo de Prompt7."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from demo.flow import (
    INVOICE_ACTIONS,
    MONTHLY_ACTIONS,
    NEED_TRANSACTIONS_ACTIONS,
    SAVINGS_BRIDGE_ACTIONS,
    SAVINGS_PLAN_ACTIONS,
    VOICE_ACTIONS,
    DemoStage,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _app() -> AppTest:
    return AppTest.from_file(
        str(PROJECT_ROOT / "streamlit_app.py"),
        default_timeout=10,
    ).run()


def _click(app: AppTest, label: str) -> None:
    next(button for button in app.button if button.label == label).click().run()


def test_main_story_reaches_real_monthly_analysis() -> None:
    app = _app()

    assert app.session_state["demo_stage"] == DemoStage.START.value
    assert app.session_state["active_suggested_actions"] == []
    assert any(
        markdown.value == "**CONTEXTO ACTUAL**"
        for markdown in app.markdown
    )
    assert all(
        "No proporciona asesoramiento" not in text
        for text in [item.value for item in app.caption]
    )
    assert len(app.chat_input) == 1
    _click(app, "Factura electricidad — septiembre")

    assert app.session_state["demo_stage"] == DemoStage.INVOICE.value
    assert app.session_state["context_items"] == [
        "factura_electricidad_septiembre.pdf"
    ]
    assert app.session_state["active_suggested_actions"] == INVOICE_ACTIONS
    assert len(app.chat_input) == 1

    _click(app, "Ver su impacto en mis gastos")
    assert app.session_state["demo_stage"] == DemoStage.NEED_TRANSACTIONS.value
    assert app.session_state["active_suggested_actions"] == (
        NEED_TRANSACTIONS_ACTIONS
    )

    _click(app, "Analizar movimientos")
    assert app.session_state["demo_stage"] == DemoStage.MONTHLY_ANALYSIS.value
    assert app.session_state["context_items"] == [
        "factura_electricidad_septiembre.pdf",
        "movimientos_septiembre.csv",
    ]
    assert app.session_state["active_suggested_actions"] == MONTHLY_ACTIONS
    assert [metric.value for metric in app.metric] == [
        "2.450 €",
        "1.780 €",
        "670 €",
        "27,3 %",
    ]
    assert len(app.get("plotly_chart")) == 1
    assert len(app.chat_input) == 1


def test_voice_savings_and_audio_states_replace_actions() -> None:
    app = _app()
    app.session_state["context_items"] = ["movimientos_septiembre.csv"]
    app.session_state["processed_uploads"] = ["movimientos_septiembre.csv"]
    app.session_state["active_scenario"] = "voice_restaurant"
    app.session_state["active_analysis"] = {
        "model_output": "Respuesta de voz",
        "suggested_actions": VOICE_ACTIONS,
    }
    app.session_state["active_suggested_actions"] = list(VOICE_ACTIONS)
    app.session_state["demo_stage"] = DemoStage.VOICE_ANALYSIS.value
    app.run()

    _click(app, "Simular impacto sobre mi ahorro")
    assert app.session_state["demo_stage"] == DemoStage.SAVINGS_BRIDGE.value
    assert app.session_state["active_suggested_actions"] == (
        SAVINGS_BRIDGE_ACTIONS
    )

    _click(app, "Explorar objetivo de ahorro")
    assert app.session_state["demo_stage"] == DemoStage.SAVINGS_PLAN.value
    assert app.session_state["active_suggested_actions"] == SAVINGS_PLAN_ACTIONS
    assert any(
        "Python" in caption.value
        for caption in app.caption
    )

    _click(app, "Escuchar resumen")
    assert app.session_state["demo_stage"] == DemoStage.SUMMARY_AUDIO.value
    assert app.session_state["active_suggested_actions"] == []
    assert len(app.get("audio")) == 1
    assert app.get("audio")[0].proto.autoplay

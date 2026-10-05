"""Prueba funcional del reinicio desde la interfaz Streamlit."""

from __future__ import annotations

from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.components.conversation import INITIAL_ASSISTANT_MESSAGE
from demo.loader import (
    load_invoice_analysis,
    load_monthly_analysis,
    load_receipt_analysis,
)
from processors.csv import analyze_transactions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = (
    PROJECT_ROOT
    / "demo_data"
    / "transactions"
    / "movimientos_septiembre.csv"
)


def _seed_analysis(
    app: AppTest,
    filename: str,
    scenario: str,
    analysis: dict,
    csv_analysis: dict | None = None,
) -> None:
    app.session_state["context_items"] = [filename]
    app.session_state["processed_uploads"] = [filename]
    app.session_state["active_scenario"] = scenario
    app.session_state["active_analysis"] = analysis
    app.session_state["csv_analysis"] = csv_analysis
    app.session_state["agent_trace"] = list(analysis.get("agent_trace", []))
    app.session_state["active_suggested_actions"] = list(
        analysis.get("suggested_actions", [])
    )
    app.run()


def test_new_conversation_resets_ui_and_allows_reuse() -> None:
    app = AppTest.from_file(
        str(PROJECT_ROOT / "streamlit_app.py"),
        default_timeout=10,
    ).run()

    assert not app.exception
    assert app.chat_input[0].placeholder == "Pregunta lo que quieras"
    assert app.chat_input[0].proto.accept_file
    assert app.chat_input[0].proto.accept_audio
    assert any(
        button.label == "Nueva conversación"
        for button in app.button
    )
    assert any(button.label == "🔊" for button in app.button)
    assert any(
        markdown.value == "## Aeraris AI"
        for markdown in app.markdown
    )

    monthly = load_monthly_analysis()
    _seed_analysis(
        app,
        "movimientos_septiembre.csv",
        "monthly",
        monthly,
        analyze_transactions(CSV_PATH).model_dump(),
    )

    assert not app.exception
    assert app.session_state["context_items"] == [
        "movimientos_septiembre.csv"
    ]
    assert app.session_state["active_scenario"] == "monthly"
    assert len(app.metric) == 4
    assert [metric.value for metric in app.metric] == [
        "2.450 €",
        "1.780 €",
        "670 €",
        "27,3 %",
    ]
    assert len(app.get("plotly_chart")) == 1
    assert len(app.get("audio")) == 0
    next(button for button in app.button if button.label == "🔊").click().run()
    assert not app.exception
    assert len(app.get("audio")) == 1
    assert getattr(app.get("audio")[0].proto, "autoplay", False)
    assert any(
        caption.value == "Puedes seguir con:"
        for caption in app.caption
    )
    assert app.get("chat_input")[0].value is None

    next(
        button
        for button in app.button
        if button.label == "Nueva conversación"
    ).click().run()

    assert not app.exception
    assert app.session_state["context_items"] == []
    assert app.session_state["active_scenario"] is None
    assert app.session_state["active_analysis"] == {}
    assert app.session_state["csv_analysis"] is None
    assert app.session_state["processed_uploads"] == []
    assert app.session_state["active_suggested_actions"] == []
    assert app.session_state["messages"] == [
        {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
    ]
    assert len(app.metric) == 0
    assert len(app.get("plotly_chart")) == 0
    assert app.get("chat_input")[0].value is None

    invoice = load_invoice_analysis()
    _seed_analysis(
        app,
        "factura_electricidad_septiembre.pdf",
        "invoice",
        invoice,
    )

    assert not app.exception
    assert app.session_state["context_items"] == [
        "factura_electricidad_septiembre.pdf"
    ]
    assert app.session_state["active_scenario"] == "invoice"
    assert len(app.metric) == 3
    assert [metric.value for metric in app.metric] == [
        "267 kWh",
        "91,24 €",
        "18/10/2026",
    ]

    assert app.get("chat_input")[0].value is None


def test_receipt_action_replaces_previous_suggestions() -> None:
    app = AppTest.from_file(
        str(PROJECT_ROOT / "streamlit_app.py"),
        default_timeout=10,
    ).run()
    receipt = load_receipt_analysis()
    _seed_analysis(
        app,
        "ticket_restaurante.pdf",
        "receipt",
        receipt,
    )

    initial_actions = {
        "Incorporar el gasto al análisis mensual",
        "Compararlo con otros gastos de restauración",
        "Ver cuánto llevo gastado en esta categoría",
    }
    assert not app.exception
    assert set(app.session_state["active_suggested_actions"]) == initial_actions
    assert sum(
        markdown.value.startswith("He identificado un gasto de restauración")
        for markdown in app.markdown
    ) == 1

    next(
        button
        for button in app.button
        if button.label == "Compararlo con otros gastos de restauración"
    ).click().run()

    new_actions = {
        "Comparar restauración con ocio",
        "Ver cuánto ha aumentado",
        "Simular impacto sobre mi ahorro",
    }
    visible_buttons = {button.label for button in app.button}
    response = app.session_state["active_analysis"]["assistant_response"]

    assert not app.exception
    assert app.session_state["active_scenario"] == "receipt_action"
    assert set(app.session_state["active_suggested_actions"]) == new_actions
    assert initial_actions.isdisjoint(visible_buttons)
    assert new_actions <= visible_buttons
    assert response != (
        "He identificado un gasto de restauración de 47,80 € realizado "
        "en La Terraza el 7 de septiembre de 2026."
    )
    assert "168 €" in response
    assert "196 €" in response
    assert "214 €" in response
    assert len(app.get("plotly_chart")) == 1
    assert sum(
        markdown.value.startswith("He identificado un gasto de restauración")
        for markdown in app.markdown
    ) == 1
    assert sum(
        caption.value == "Puedes seguir con:"
        for caption in app.caption
    ) == 1

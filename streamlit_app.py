"""Experiencia conversacional de Aeraris AI."""

from __future__ import annotations

import inspect

import streamlit as st

from app.components.agent_trace import render_agent_trace
from app.components.audio import render_audio_output
from app.components.context_panel import render_context_panel
from app.components.conversation import render_conversation
from app.components.research import (
    render_infographic_progress,
    render_research_progress,
)
from app.components.scenario_results import render_active_analysis
from app.components.suggested_actions import render_suggested_actions
from app.components.uploader import render_file_uploader
from app.session import (
    complete_infographic_generation,
    complete_web_research,
    current_upload_widget_key,
    handle_composer_submission,
    handle_demo_document,
    handle_question,
    handle_suggested_action,
    handle_summary_audio,
    handle_upload,
    handle_voice_demo,
    initialize_session_state,
    reset_session,
)
from core.config import APP_NAME, APP_SUBTITLE
from demo.flow import DemoStage

AUDIO_RENDERED_SESSION_KEY = "_audio_rendered_this_run"

LAYOUT_STYLES = """
<style>
    [data-testid="stMain"] {
        overflow: hidden;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 100%;
        height: 100vh;
        overflow: hidden;
        padding: 1rem 2rem 0.75rem;
    }

    .st-key-sidebar_footer {
        width: 100%;
        margin-top: 1rem;
    }

    .st-key-sidebar_footer [data-testid="stButton"] button {
        width: 100%;
    }

    .st-key-suggested_actions_panel {
        position: fixed;
        left: 23vw;
        right: 2rem;
        width: auto !important;
        max-width: calc(100vw - 23vw - 2rem);
        min-width: 0 !important;
        box-sizing: border-box;
        bottom: 5.25rem;
        z-index: 20;
        padding: 0.25rem 0;
        overflow-x: hidden;
        background: var(--background-color, #ffffff);
    }

    .st-key-interaction_panel {
        position: fixed;
        left: 23vw;
        right: 2rem;
        width: auto !important;
        max-width: calc(100vw - 23vw - 2rem);
        min-width: 0 !important;
        box-sizing: border-box;
        bottom: 0.75rem;
        z-index: 21;
        padding-top: 0.35rem;
        overflow-x: hidden;
        background: var(--background-color, #ffffff);
    }

    .st-key-suggested_actions_panel > div,
    .st-key-interaction_panel > div,
    .st-key-suggested_actions_panel [data-testid="stHorizontalBlock"],
    .st-key-interaction_panel [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box;
    }

    .st-key-suggested_actions_panel [data-testid="column"],
    .st-key-interaction_panel [data-testid="column"] {
        min-width: 0 !important;
        max-width: 100% !important;
        box-sizing: border-box;
    }

    .st-key-suggested_actions_panel button {
        width: 100%;
        min-width: 0;
        height: auto;
        white-space: normal;
        overflow-wrap: anywhere;
    }

    .st-key-interaction_panel [data-testid="stChatInput"] {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box;
    }

    .st-key-speak_summary button {
        min-height: 3.25rem;
        padding: 0.5rem;
        border-radius: 999px;
        font-size: 1.15rem;
    }
</style>
"""


def main() -> None:
    """Compone la experiencia B2C a partir de componentes pequeños."""
    st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide")
    st.markdown(LAYOUT_STYLES, unsafe_allow_html=True)
    st.session_state[AUDIO_RENDERED_SESSION_KEY] = False
    initialize_session_state()

    sidebar_column, conversation_column = st.columns(
        [1.15, 3.85],
        gap="large",
    )

    with sidebar_column:
        st.markdown(f"## {APP_NAME}")
        st.markdown(
            f"**{APP_SUBTITLE}** · "
            "Entiende tus finanzas. Pregunta como quieras."
        )
        selected_document = render_context_panel()
        if selected_document and handle_demo_document(selected_document):
            st.rerun()

        with st.container(key="sidebar_footer"):
            if st.button(
                "Nueva conversación",
                key="new_conversation",
                type="secondary",
                use_container_width=True,
            ):
                reset_session()
                st.rerun()

    with conversation_column:
        conversation_area = _create_container(
            height=500,
            border=True,
            key="conversation_history",
            autoscroll=True,
        )
        actions_area = _create_container(key="suggested_actions_panel")

        with _create_container(key="interaction_panel"):
            composer_column, speaker_column = st.columns(
                [18, 1],
                gap="small",
            )
            with composer_column:
                native_media = _supports_native_media_composer()
                if native_media:
                    submission = st.chat_input(
                        "Pregunta lo que quieras",
                        key=current_upload_widget_key(),
                        accept_file=True,
                        file_type=["pdf", "png", "jpg", "jpeg", "csv"],
                        accept_audio=True,
                    )
                    uploaded_file = None
                    voice_requested = False
                    question = None
                else:
                    fallback_column, fallback_voice = st.columns([4, 1])
                    with fallback_column:
                        uploaded_file = render_file_uploader(
                            "Añadir archivo",
                            ["pdf", "png", "jpg", "jpeg", "csv"],
                            current_upload_widget_key(),
                        )
                    with fallback_voice:
                        voice_requested = st.button(
                            "🎤 Hablar",
                            key="voice_action",
                            type="secondary",
                            use_container_width=True,
                        )
                    if hasattr(st, "chat_input"):
                        question = st.chat_input(
                            "Pregunta lo que quieras",
                            key="conversation_question",
                        )
                    else:
                        draft_question = st.text_input(
                            "Pregunta lo que quieras",
                            key="conversation_question",
                        )
                        question = (
                            draft_question
                            if st.button(
                                "Enviar",
                                key="conversation_submit",
                            )
                            else None
                        )
                    submission = None
            with speaker_column:
                speak_requested = st.button(
                    "🔊",
                    help="Escuchar el resumen hablado",
                    key="speak_summary",
                    type="primary",
                    use_container_width=True,
                )

        if native_media:
            handle_composer_submission(submission)
        else:
            handle_upload(uploaded_file)
            if voice_requested:
                handle_voice_demo()
            handle_question(question)
        monthly_audio_available = (
            st.session_state.active_scenario == "monthly"
            or "movimientos_septiembre.csv"
            in st.session_state.context_items
        )
        if speak_requested and monthly_audio_available:
            handle_summary_audio()
        elif speak_requested:
            st.toast(
                "Añade los movimientos de septiembre para escuchar su resumen."
            )

        with conversation_area:
            render_conversation()
            current_stage = st.session_state.get(
                "demo_stage",
                DemoStage.START.value,
            )
            if current_stage == DemoStage.WEB_RESEARCH.value:
                render_research_progress()
                complete_web_research()
                st.rerun()
            if current_stage == DemoStage.INFOGRAPHIC_GENERATION.value:
                render_infographic_progress()
                complete_infographic_generation()
                st.rerun()
            render_active_analysis(
                st.session_state.active_scenario,
                st.session_state.active_analysis,
                st.session_state.csv_analysis,
                autoplay_audio=speak_requested and monthly_audio_available,
            )
            show_monthly_audio = (
                monthly_audio_available
                and st.session_state.active_scenario == "monthly"
                and speak_requested
            )
            show_summary_audio = (
                st.session_state.active_scenario == "summary_audio"
            )
            if show_monthly_audio or show_summary_audio:
                with st.chat_message("assistant"):
                    render_audio_output(
                        autoplay=speak_requested or show_summary_audio,
                    )
            render_agent_trace(st.session_state.agent_trace)
        with actions_area:
            selected_action = render_suggested_actions(
                list(st.session_state.active_suggested_actions)
            )
        if handle_suggested_action(selected_action):
            st.rerun()


def _create_container(**kwargs):
    """Usa solo los parámetros de layout disponibles en la versión instalada."""
    supported = inspect.signature(st.container).parameters
    return st.container(
        **{key: value for key, value in kwargs.items() if key in supported}
    )


def _supports_native_media_composer() -> bool:
    """Detecta si Streamlit ofrece archivos y audio en chat_input."""
    if not hasattr(st, "chat_input"):
        return False
    supported = inspect.signature(st.chat_input).parameters
    return "accept_file" in supported and "accept_audio" in supported


if __name__ == "__main__":
    main()

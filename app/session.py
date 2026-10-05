"""Estado efímero y eventos de la demostración conversacional."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from app.components.conversation import INITIAL_ASSISTANT_MESSAGE, add_message
from demo.actions import resolve_suggested_action
from demo.infographic import (
    INFOGRAPHIC_PATH,
    build_execution_trace as build_infographic_trace,
    is_infographic_confirmation,
)
from demo.flow import (
    INVOICE_ACTIONS,
    MONTHLY_ACTIONS,
    NEED_TRANSACTIONS_ACTIONS,
    SAVINGS_BRIDGE_ACTIONS,
    SAVINGS_PLAN_ACTIONS,
    VOICE_ACTIONS,
    DemoStage,
    document_label,
    stage_for_scenario,
)
from demo.research import (
    build_execution_trace as build_research_trace,
    build_research_markdown,
    is_compound_interest_query,
    load_compound_interest_research,
)
from demo.loader import (
    load_analysis_for_file,
    load_savings_plan,
    load_voice_analysis,
)
from processors.csv import analyze_transactions

TRANSACTIONS_DIR = Path(__file__).resolve().parents[1] / "demo_data" / "transactions"

UNSUPPORTED_FILE_MESSAGE = (
    "Todavía no puedo analizar este archivo. Prueba con una factura, "
    "un ticket o movimientos compatibles."
)

SESSION_DEFAULTS: dict[str, Any] = {
    "context_items": [],
    "processed_uploads": [],
    "active_scenario": None,
    "active_analysis": {},
    "csv_analysis": None,
    "agent_trace": [],
    "active_suggested_actions": [],
    "upload_widget_version": 0,
    "demo_stage": DemoStage.START.value,
    "voice_prompt_pending": False,
    "research_offer_active": False,
}

FILE_UPLOADER_KEY_PREFIX = "conversation_attachment"

TRANSIENT_WIDGET_KEYS = (
    FILE_UPLOADER_KEY_PREFIX,
    "voice_action",
    "conversation_question",
    "conversation_submit",
    "speak_summary",
    "suggested_action_0",
    "suggested_action_1",
    "suggested_action_2",
)


def initialize_session_state() -> None:
    """Inicializa el contexto temporal de la experiencia conversacional."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
        ]
    for key, value in _fresh_session_defaults().items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session() -> None:
    """Restaura una conversación vacía sin borrar configuración global."""
    next_upload_version = (
        int(st.session_state.get("upload_widget_version", 0)) + 1
    )
    conversation_keys = (
        "messages",
        *SESSION_DEFAULTS,
        *TRANSIENT_WIDGET_KEYS,
    )
    for key in list(st.session_state):
        is_upload_widget = key.startswith(f"{FILE_UPLOADER_KEY_PREFIX}_")
        if key in conversation_keys or is_upload_widget:
            del st.session_state[key]

    st.session_state["messages"] = [
        {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
    ]
    for key, value in _fresh_session_defaults().items():
        st.session_state[key] = value
    st.session_state["upload_widget_version"] = next_upload_version


def current_upload_widget_key() -> str:
    """Genera una identidad renovable para vaciar el cargador de archivos."""
    version = int(st.session_state.get("upload_widget_version", 0))
    return f"{FILE_UPLOADER_KEY_PREFIX}_{version}"


def handle_upload(
    uploaded_file: Any | None,
    user_message: str | None = None,
) -> None:
    """Integra un adjunto preparado sin repetirlo durante los rerenders."""
    if uploaded_file is None:
        return

    filename = uploaded_file.name
    _process_filename(
        filename,
        source=uploaded_file,
        user_message=user_message or f"He adjuntado {filename}",
    )


def handle_demo_document(filename: str) -> bool:
    """Activa un documento incluido en la demo desde el panel lateral."""
    if filename in st.session_state.processed_uploads:
        return False
    return _process_filename(
        filename,
        user_message=f"He seleccionado {document_label(filename)}",
    )


def _process_filename(
    filename: str,
    *,
    source: Any | None = None,
    user_message: str | None = None,
) -> bool:
    """Carga un escenario preparado y calcula el CSV cuando corresponde."""
    if filename in st.session_state.processed_uploads:
        return False

    st.session_state.processed_uploads.append(filename)
    if filename not in st.session_state.context_items:
        st.session_state.context_items.append(filename)
    if user_message:
        add_message("user", user_message)

    scenario_name, analysis = load_analysis_for_file(filename)
    if scenario_name is None:
        _clear_active_analysis()
        add_message("assistant", UNSUPPORTED_FILE_MESSAGE)
        return True

    if analysis.get("error"):
        _clear_active_analysis()
        add_message("assistant", str(analysis["error"]))
        return True

    csv_analysis: dict[str, Any] | None = None
    if scenario_name == "monthly":
        csv_source = source
        if csv_source is None:
            csv_source = TRANSACTIONS_DIR / filename
        try:
            csv_analysis = analyze_transactions(csv_source).model_dump()
        except Exception:
            _clear_active_analysis()
            add_message(
                "assistant",
                "No he podido calcular las métricas del archivo CSV.",
            )
            return True

    _set_active_analysis(scenario_name, analysis, csv_analysis)
    _set_demo_stage(stage_for_scenario(scenario_name))
    if scenario_name == "invoice":
        st.session_state.active_suggested_actions = list(INVOICE_ACTIONS)
    elif scenario_name == "monthly":
        st.session_state.active_suggested_actions = list(MONTHLY_ACTIONS)
    return True


def handle_composer_submission(submission: Any | None) -> None:
    """Procesa texto, archivo o audio enviados desde el compositor único."""
    if submission is None:
        return
    if isinstance(submission, str):
        handle_question(submission)
        return

    text = str(getattr(submission, "text", "") or "").strip()
    files = list(getattr(submission, "files", []) or [])
    audio = getattr(submission, "audio", None)

    if files:
        handle_upload(files[0], text or None)
        return
    if audio is not None:
        handle_voice_demo()
        return
    handle_question(text)


def handle_voice_demo() -> None:
    """Carga la transcripción y respuesta generadas para el escenario de voz."""
    analysis = load_voice_analysis()
    st.toast("Escuchando...")
    if analysis.get("error"):
        _clear_active_analysis()
        add_message("assistant", str(analysis["error"]))
        return

    _archive_active_response()
    transcription = str(
        analysis.get("speech_to_text", {}).get("transcription", "")
    )
    response = str(analysis.get("model_output", ""))
    _set_active_analysis("voice_restaurant", analysis, None)
    _set_demo_stage(DemoStage.VOICE_ANALYSIS)
    st.session_state.voice_prompt_pending = False
    st.session_state.active_suggested_actions = list(VOICE_ACTIONS)
    st.session_state.agent_trace = _voice_trace(analysis)
    if transcription:
        add_message("user", transcription)
    if response:
        add_message("assistant", response)


def handle_question(question: str | None) -> None:
    """Responde a texto libre y activa la continuación educativa contextual."""
    if not question:
        return

    stage = _current_demo_stage()
    if stage == DemoStage.RESEARCH_RESULT:
        if (
            st.session_state.get("research_offer_active", False)
            and is_infographic_confirmation(question)
        ):
            _archive_active_response()
            add_message("user", question)
            st.session_state.active_suggested_actions = []
            st.session_state.research_offer_active = False
            _set_active_analysis("infographic_generation", {}, None)
            _set_demo_stage(DemoStage.INFOGRAPHIC_GENERATION)
            return

    if stage in {DemoStage.SUMMARY_AUDIO, DemoStage.OPEN_CHAT}:
        _set_demo_stage(DemoStage.OPEN_CHAT)
        if is_compound_interest_query(question):
            add_message("user", question)
            st.session_state.active_suggested_actions = []
            st.session_state.research_offer_active = False
            _set_active_analysis("research_progress", {}, None)
            _set_demo_stage(DemoStage.WEB_RESEARCH)
            return

    analysis = st.session_state.active_analysis
    _archive_active_response()
    add_message("user", question)
    st.session_state.active_suggested_actions = []
    response = _analysis_response(analysis)
    if response:
        _set_active_analysis(
            "action_response",
            {
                "assistant_response": response,
                "suggested_actions": [],
            },
            None,
        )
        return
    _clear_active_analysis()
    add_message(
        "assistant",
        "Adjunta un documento o movimientos para contextualizar la conversación.",
    )


def complete_web_research() -> None:
    """Cierra la simulación de búsqueda y publica la respuesta precalculada."""
    research = load_compound_interest_research()
    add_message("assistant", build_research_trace())
    _set_active_analysis("research", research, None)
    _set_demo_stage(DemoStage.RESEARCH_RESULT)
    st.session_state.research_offer_active = True
    st.session_state.active_suggested_actions = []


def complete_infographic_generation() -> None:
    """Cierra la simulación visual y deja la infografía como resultado activo."""
    add_message("assistant", build_infographic_trace())
    _set_active_analysis(
        "infographic",
        {"image_path": str(INFOGRAPHIC_PATH)},
        None,
    )
    _set_demo_stage(DemoStage.INFOGRAPHIC)
    st.session_state.research_offer_active = False
    st.session_state.active_suggested_actions = []


def handle_suggested_action(action: str | None) -> bool:
    """Gestiona una transición narrativa y devuelve si debe rerenderizar."""
    if not action:
        return False

    stage = _current_demo_stage()
    current_scenario = st.session_state.active_scenario
    current_analysis = st.session_state.active_analysis
    _archive_active_response()
    add_message("user", action)
    st.session_state.active_suggested_actions = []

    if stage == DemoStage.INVOICE and action == "Ver su impacto en mis gastos":
        _set_action_response(
            "Para valorar el impacto de esta factura necesito contextualizarla "
            "con tus movimientos del mes.\n\n"
            "Tengo disponible movimientos_septiembre.csv.\n"
            "¿Quieres que lo analice?",
            NEED_TRANSACTIONS_ACTIONS,
            DemoStage.NEED_TRANSACTIONS,
        )
        return True

    if (
        stage == DemoStage.NEED_TRANSACTIONS
        and action == "Analizar movimientos"
    ):
        _process_filename("movimientos_septiembre.csv")
        _set_demo_stage(DemoStage.MONTHLY_ANALYSIS)
        st.session_state.active_suggested_actions = list(MONTHLY_ACTIONS)
        return True

    if stage == DemoStage.NEED_TRANSACTIONS and action == "Ahora no":
        _set_action_response(
            "De acuerdo. Puedes analizar tus movimientos cuando quieras.",
            INVOICE_ACTIONS,
            DemoStage.INVOICE,
        )
        return True

    if stage == DemoStage.MONTHLY_ANALYSIS and action == "Preguntar por voz":
        st.session_state.voice_prompt_pending = True
        _set_action_response(
            "Puedes preguntarme por voz.",
            [],
            DemoStage.MONTHLY_ANALYSIS,
        )
        return True

    if stage == DemoStage.MONTHLY_ANALYSIS and action == (
        "Explorar un objetivo de ahorro"
    ):
        _load_savings_plan()
        return True

    if stage == DemoStage.MONTHLY_ANALYSIS and action == (
        "Ver qué gastos han aumentado"
    ):
        _set_action_response(
            "El gasto en restauración ha aumentado un 17,6 % frente a la "
            "media de julio y agosto. Puedes preguntarme por voz para "
            "compararlo con más detalle.",
            ["Preguntar por voz", "Explorar un objetivo de ahorro"],
            DemoStage.MONTHLY_ANALYSIS,
        )
        return True

    if stage == DemoStage.VOICE_ANALYSIS and action == (
        "Simular impacto sobre mi ahorro"
    ):
        _set_action_response(
            "Reducir determinados gastos discrecionales podría aumentar tu "
            "capacidad de ahorro mensual.\n\n"
            "Actualmente has ahorrado 670 € este mes.\n"
            "¿Quieres explorar un objetivo de ahorro?",
            SAVINGS_BRIDGE_ACTIONS,
            DemoStage.SAVINGS_BRIDGE,
        )
        return True

    if stage == DemoStage.SAVINGS_BRIDGE and action == (
        "Explorar objetivo de ahorro"
    ):
        _load_savings_plan()
        return True

    if stage == DemoStage.SAVINGS_BRIDGE and action == (
        "Volver al análisis mensual"
    ):
        _restore_monthly_analysis()
        return True

    if stage == DemoStage.SAVINGS_PLAN and action == "Escuchar resumen":
        _set_summary_audio()
        return True

    if stage == DemoStage.SAVINGS_PLAN and action in {
        "Simular otro objetivo",
        "Cambiar ahorro mensual",
    }:
        _set_action_response(
            "Puedo actualizar esta simulación cuando definamos el nuevo "
            "objetivo o el ahorro mensual.",
            SAVINGS_PLAN_ACTIONS,
            DemoStage.SAVINGS_PLAN,
        )
        return True

    if stage == DemoStage.VOICE_ANALYSIS and action in {
        "Ver evolución",
        "Comparar con otras categorías",
    }:
        _set_action_response(
            "Este mes has gastado 214 € en restauración, frente a una media "
            "reciente de 182 €. La comparación ayuda a observar la tendencia "
            "sin convertirla en una conclusión absoluta.",
            VOICE_ACTIONS,
            DemoStage.VOICE_ANALYSIS,
        )
        return True

    action_result = resolve_suggested_action(action, current_scenario)
    if action_result is not None:
        _set_active_analysis("receipt_action", action_result, None)
        _set_demo_stage(DemoStage.RECEIPT)
        return True

    if _is_savings_action(action):
        _load_savings_plan()
        return True

    response = _analysis_response(current_analysis)
    if response:
        _set_active_analysis(
            "action_response",
            {
                "assistant_response": response,
                "suggested_actions": [],
            },
            None,
        )
        _set_demo_stage(stage)
        return True
    _clear_active_analysis()
    return True


def handle_summary_audio() -> bool:
    """Activa el resumen hablado si los movimientos están en el contexto."""
    if "movimientos_septiembre.csv" not in st.session_state.context_items:
        return False
    if (
        st.session_state.active_scenario == "monthly"
    ):
        # El botón fijo de altavoz reproduce el audio dentro del análisis
        # mensual sin retirar sus acciones contextuales.
        return True
    _set_summary_audio()
    return True


def _load_savings_plan() -> None:
    analysis = load_savings_plan()
    if analysis.get("error"):
        _clear_active_analysis()
        add_message("assistant", str(analysis["error"]))
        return
    _set_active_analysis("savings", analysis, None)
    _set_demo_stage(DemoStage.SAVINGS_PLAN)
    st.session_state.active_suggested_actions = list(SAVINGS_PLAN_ACTIONS)


def _restore_monthly_analysis() -> None:
    analysis = load_analysis_for_file("movimientos_septiembre.csv")[1]
    try:
        csv_analysis = analyze_transactions(
            TRANSACTIONS_DIR / "movimientos_septiembre.csv"
        ).model_dump()
    except Exception:
        _clear_active_analysis()
        add_message(
            "assistant",
            "No he podido calcular las métricas del archivo CSV.",
        )
        return
    _set_active_analysis("monthly", analysis, csv_analysis)
    _set_demo_stage(DemoStage.MONTHLY_ANALYSIS)
    st.session_state.active_suggested_actions = list(MONTHLY_ACTIONS)


def _set_action_response(
    response: str,
    actions: list[str],
    stage: DemoStage,
) -> None:
    _set_active_analysis(
        "action_response",
        {
            "assistant_response": response,
            "suggested_actions": list(actions),
        },
        None,
    )
    _set_demo_stage(stage)


def _set_summary_audio() -> None:
    _set_active_analysis(
        "summary_audio",
        {"suggested_actions": []},
        None,
    )
    _set_demo_stage(DemoStage.SUMMARY_AUDIO)
    st.session_state.active_suggested_actions = []


def _set_demo_stage(stage: DemoStage) -> None:
    st.session_state.demo_stage = stage.value


def _current_demo_stage() -> DemoStage:
    value = st.session_state.get("demo_stage", DemoStage.START.value)
    try:
        return DemoStage(value)
    except ValueError:
        return DemoStage.START


def _set_active_analysis(
    scenario_name: str,
    analysis: dict[str, Any],
    csv_analysis: dict[str, Any] | None,
) -> None:
    st.session_state.active_scenario = scenario_name
    st.session_state.active_analysis = analysis
    st.session_state.csv_analysis = csv_analysis
    st.session_state.agent_trace = list(analysis.get("agent_trace", []))
    st.session_state.active_suggested_actions = list(
        analysis.get("suggested_actions", [])
    )
    if scenario_name not in {"research", "research_progress"}:
        st.session_state.research_offer_active = False


def _clear_active_analysis() -> None:
    st.session_state.active_scenario = None
    st.session_state.active_analysis = {}
    st.session_state.csv_analysis = None
    st.session_state.agent_trace = []
    st.session_state.active_suggested_actions = []
    st.session_state.voice_prompt_pending = False
    st.session_state.research_offer_active = False
    _set_demo_stage(DemoStage.START)


def _is_savings_action(action: str) -> bool:
    normalized = action.casefold()
    return "objetivo" in normalized and "ahorro" in normalized


def _archive_active_response() -> None:
    """Conserva el texto de una respuesta enriquecida antes de sustituirla."""
    rich_scenarios = {
        "invoice",
        "receipt",
        "monthly",
        "savings",
        "receipt_action",
        "action_response",
        "research",
        "infographic",
    }
    if st.session_state.active_scenario not in rich_scenarios:
        return

    if st.session_state.active_scenario == "research":
        response = build_research_markdown(
            st.session_state.active_analysis,
        )
    elif st.session_state.active_scenario == "infographic":
        response = "He preparado una versión visual sencilla del ejemplo."
    else:
        response = _analysis_response(st.session_state.active_analysis)
    if not response:
        return
    messages = st.session_state.messages
    if messages and messages[-1] == {"role": "assistant", "content": response}:
        return
    add_message("assistant", response)


def _analysis_response(analysis: dict[str, Any]) -> str:
    response = (
        analysis.get("assistant_response")
        or analysis.get("summary")
        or analysis.get("model_output")
    )
    return str(response) if response else ""


def _voice_trace(analysis: dict[str, Any]) -> list[str]:
    selected_tools = analysis.get("agent_reasoning_summary", {}).get(
        "tools_selected",
        [],
    )
    tool_steps = {
        "transaction_analyzer": "Consultando movimientos",
        "financial_calculator": "Comparando con el histórico",
        "financial_explainer": "Preparando explicación",
    }
    steps = ["Analizando tu pregunta"]
    steps.extend(
        tool_steps[tool]
        for tool in selected_tools
        if tool in tool_steps
    )
    return steps


def _fresh_session_defaults() -> dict[str, Any]:
    """Devuelve contenedores nuevos para evitar estado mutable compartido."""
    return {
        key: value.copy() if isinstance(value, (dict, list)) else value
        for key, value in SESSION_DEFAULTS.items()
    }

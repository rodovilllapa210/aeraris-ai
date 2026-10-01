"""Punto de entrada único desde la UI a la lógica de negocio."""

from __future__ import annotations

from collections.abc import Callable

from core.rules import evaluate_financial_rules
from core.schemas import (
    AnalysisRequest,
    AnalysisResult,
    AnalysisStatus,
    ChatRequest,
    ChatResponse,
    InputType,
)
from models.llm import answer_question, generate_summary, suggest_questions
from processors.csv import process_csv
from processors.image import process_image
from processors.pdf import process_pdf
from visualizations.charts import create_chart_specs


def analyse(request: AnalysisRequest) -> AnalysisResult:
    """Procesa una solicitud y siempre devuelve un resultado controlado."""
    try:
        result = _dispatch(request)
        return _enrich(result)
    except Exception as exc:  # Frontera defensiva: no propagar errores a la UI.
        return AnalysisResult(
            status=AnalysisStatus.ERROR,
            input_type=request.input_type,
            source_name=request.source_name,
            errors=[f"No se pudo completar el análisis: {exc}"],
        )


def chat(request: ChatRequest) -> ChatResponse:
    """Responde usando una representación JSON sencilla del análisis."""
    try:
        context = request.context.model_dump_json(indent=2)
        return ChatResponse(
            answer=answer_question(request.question, context),
            suggested_questions=request.context.suggested_questions,
        )
    except Exception as exc:
        return ChatResponse(answer="", error=f"No se pudo responder: {exc}")


def _dispatch(request: AnalysisRequest) -> AnalysisResult:
    processors: dict[InputType, Callable[[str], AnalysisResult]] = {
        InputType.PDF: process_pdf,
        InputType.IMAGE: process_image,
        InputType.CSV: process_csv,
    }

    if request.input_type in processors:
        if not request.file_path:
            raise ValueError("La ruta del archivo es obligatoria para este tipo de entrada.")
        return processors[request.input_type](request.file_path)

    if request.input_type == InputType.TEXT:
        return AnalysisResult(
            input_type=InputType.TEXT,
            source_name=request.source_name,
            extracted_text=request.text,
        )

    return AnalysisResult(
        status=AnalysisStatus.PARTIAL,
        input_type=InputType.AUDIO,
        source_name=request.source_name,
        summary="[MOCK] La entrada de audio todavía no está integrada.",
    )


def _enrich(result: AnalysisResult) -> AnalysisResult:
    steps: tuple[tuple[str, Callable[[], object]], ...] = (
        ("summary", lambda: generate_summary(result.data, result.extracted_text)),
        ("warnings", lambda: evaluate_financial_rules(result.data)),
        ("suggested_questions", lambda: suggest_questions(result.data)),
        ("charts", lambda: create_chart_specs(result.data)),
    )

    for field_name, operation in steps:
        try:
            generated_value = operation()
            if field_name == "summary" and result.summary:
                continue
            setattr(result, field_name, generated_value)
        except Exception as exc:
            result.errors.append(f"Error al generar {field_name}: {exc}")
            if result.status == AnalysisStatus.SUCCESS:
                result.status = AnalysisStatus.PARTIAL
    return result

"""Procesador PDF pendiente de implementación."""

from __future__ import annotations

from pathlib import Path

from core.schemas import AnalysisResult, AnalysisStatus, InputType


def process_pdf(file_path: str) -> AnalysisResult:
    """Devuelve un resultado controlado hasta integrar el procesamiento PDF."""
    return AnalysisResult(
        input_type=InputType.PDF,
        source_name=Path(file_path).name,
        status=AnalysisStatus.PARTIAL,
        summary="[MOCK] El procesador PDF todavía es un stub.",
    )

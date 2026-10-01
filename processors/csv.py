"""Procesador CSV pendiente de implementación."""

from __future__ import annotations

from pathlib import Path

from core.schemas import AnalysisResult, AnalysisStatus, InputType


def process_csv(file_path: str) -> AnalysisResult:
    """Devuelve un resultado controlado hasta integrar el procesamiento CSV."""
    return AnalysisResult(
        input_type=InputType.CSV,
        source_name=Path(file_path).name,
        status=AnalysisStatus.PARTIAL,
        summary="[MOCK] El procesador CSV todavía es un stub.",
    )

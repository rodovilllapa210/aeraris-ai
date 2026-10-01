"""Procesador de imágenes pendiente de implementación."""

from __future__ import annotations

from pathlib import Path

from core.schemas import AnalysisResult, AnalysisStatus, InputType


def process_image(file_path: str) -> AnalysisResult:
    """Devuelve un resultado controlado hasta integrar visión u OCR."""
    return AnalysisResult(
        input_type=InputType.IMAGE,
        source_name=Path(file_path).name,
        status=AnalysisStatus.PARTIAL,
        summary="[MOCK] El procesador de imágenes todavía es un stub.",
    )

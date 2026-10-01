"""Stubs controlados de reconocimiento y síntesis de voz."""

from __future__ import annotations

from core.schemas import SpeechResult, TranscriptionResult


def speech_to_text(audio_path: str) -> TranscriptionResult:
    """Informa de que el reconocimiento de voz aún no está integrado."""
    return TranscriptionResult(
        text="",
        error="[MOCK] La transcripción de audio todavía no está disponible.",
    )


def text_to_speech(text: str) -> SpeechResult:
    """Informa de que la síntesis de voz aún no está integrada."""
    return SpeechResult(
        error="[MOCK] La síntesis de voz todavía no está disponible.",
    )

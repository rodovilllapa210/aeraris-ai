"""Salida de audio opcional para la demostración."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

DEFAULT_AUDIO_PATH = Path("demo_data/audio/audio_resumen_septiembre.wav")
AUDIO_RENDERED_SESSION_KEY = "_audio_rendered_this_run"


def render_audio_output(
    audio_path: str | Path = DEFAULT_AUDIO_PATH,
    *,
    autoplay: bool = False,
) -> None:
    """Reproduce el resumen si existe y tolera que el asset aún no esté cargado."""
    st.markdown("**🔊 Resumen hablado**")
    path = Path(audio_path)
    if path.is_file():
        if st.session_state.get(AUDIO_RENDERED_SESSION_KEY, False):
            return
        st.session_state[AUDIO_RENDERED_SESSION_KEY] = True
        st.audio(
            str(path),
            format="audio/wav",
            autoplay=autoplay,
        )
        return

    st.caption("El resumen de audio no está disponible en este momento.")

"""Aplicación Streamlit mínima de Aeraris AI."""

from __future__ import annotations

import streamlit as st

from app.components.chat import render_chat_input
from app.components.results import render_analysis_result
from app.components.uploader import render_file_uploader
from core.config import APP_NAME, APP_SUBTITLE
from tests.mocks import mock_invoice_result


def main() -> None:
    """Renderiza la interfaz inicial del MVP."""
    st.set_page_config(page_title=APP_NAME, page_icon="✈️", layout="wide")
    st.title(APP_NAME)
    st.subheader(APP_SUBTITLE)
    st.write(
        "MVP multimodal para centralizar el análisis financiero de una PYME "
        "a partir de documentos, imágenes, datos, voz y texto."
    )

    document_tab, image_tab, csv_tab, voice_tab, text_tab = st.tabs(
        ["Documento", "Imagen", "CSV", "Voz", "Texto"]
    )

    with document_tab:
        render_file_uploader("Sube un documento PDF", ["pdf"], "document")
    with image_tab:
        render_file_uploader("Sube una imagen", ["png", "jpg", "jpeg"], "image")
    with csv_tab:
        render_file_uploader("Sube un archivo CSV", ["csv"], "csv")
    with voice_tab:
        st.info("La entrada por voz se integrará en una fase posterior.")
    with text_tab:
        st.text_area("Introduce texto financiero", key="financial_text")

    st.divider()
    demo_enabled = st.toggle("Modo demostración", value=True)
    if demo_enabled:
        st.header("Factura de demostración")
        demo_result = mock_invoice_result()
        render_analysis_result(demo_result)
        render_chat_input()


if __name__ == "__main__":
    main()

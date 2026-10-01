"""Componentes de carga de archivos."""

from __future__ import annotations

from typing import Any

import streamlit as st


def render_file_uploader(
    label: str,
    file_types: list[str],
    key: str,
) -> Any | None:
    """Muestra un cargador y devuelve el archivo recibido, si existe."""
    return st.file_uploader(label, type=file_types, key=key)

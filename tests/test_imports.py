"""Pruebas de importación del scaffold compartido."""

from __future__ import annotations

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "core.schemas",
        "core.orchestrator",
        "processors.pdf",
        "processors.image",
        "processors.csv",
        "models.llm",
        "models.speech",
        "visualizations.charts",
    ],
)
def test_module_imports(module_name: str) -> None:
    assert importlib.import_module(module_name) is not None

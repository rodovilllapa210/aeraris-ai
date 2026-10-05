"""Pruebas de importación del scaffold compartido."""

from __future__ import annotations

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "core.schemas",
        "core.orchestrator",
        "app.session",
        "app.components.agent_trace",
        "app.components.audio",
        "app.components.context_panel",
        "app.components.conversation",
        "app.components.dashboard",
        "app.components.research",
        "app.components.scenario_results",
        "app.components.suggested_actions",
        "demo.actions",
        "demo.flow",
        "demo.loader",
        "demo.research",
        "demo.infographic",
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

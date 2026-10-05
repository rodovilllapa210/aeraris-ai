"""Carga controlada de los outputs generados para la demostración."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = REPOSITORY_ROOT / "demo_data" / "outputs"

SCENARIO_FILES = {
    "invoice": "invoice_analysis.json",
    "receipt": "receipt_analysis.json",
    "monthly": "monthly_analysis.json",
    "voice_restaurant": "voice_restaurant_output.json",
    "savings": "savings_plan_output.json",
}


FILE_SCENARIOS = {
    "factura_electricidad_septiembre.pdf": "invoice",
    "ticket_restaurante.png": "receipt",
    "ticket_restaurante.pdf": "receipt",
    "movimientos_septiembre.csv": "monthly",
}


def load_scenario(filename: str) -> dict[str, Any]:
    """Carga un JSON de outputs o devuelve un error apto para la UI."""
    if Path(filename).name != filename:
        return _error_result("La ruta del escenario no es válida.")

    path = OUTPUTS_DIR / filename
    try:
        with path.open(encoding="utf-8") as file:
            payload = json.load(file)
    except FileNotFoundError:
        return _error_result(f"No se encuentra el escenario {filename}.")
    except (OSError, json.JSONDecodeError):
        return _error_result(f"No se ha podido leer el escenario {filename}.")

    if not isinstance(payload, dict):
        return _error_result(f"El escenario {filename} no tiene un formato válido.")
    return payload


def load_invoice_analysis() -> dict[str, Any]:
    return load_scenario(SCENARIO_FILES["invoice"])


def load_receipt_analysis() -> dict[str, Any]:
    return load_scenario(SCENARIO_FILES["receipt"])


def load_monthly_analysis() -> dict[str, Any]:
    return load_scenario(SCENARIO_FILES["monthly"])


def load_voice_analysis() -> dict[str, Any]:
    return load_scenario(SCENARIO_FILES["voice_restaurant"])


def load_savings_plan() -> dict[str, Any]:
    return load_scenario(SCENARIO_FILES["savings"])


def detect_scenario(filename: str) -> str | None:
    """Detecta únicamente los nombres de archivo preparados para la demo."""
    return FILE_SCENARIOS.get(Path(filename).name.casefold())


def get_scenario(name: str) -> dict[str, Any]:
    """Carga un escenario por su nombre lógico."""
    filename = SCENARIO_FILES.get(name)
    if filename is None:
        return _error_result(f"Escenario desconocido: {name}.")
    return load_scenario(filename)


def load_analysis_for_file(filename: str) -> tuple[str | None, dict[str, Any]]:
    """Detecta y carga el output asociado a un archivo de entrada."""
    scenario_name = detect_scenario(filename)
    if scenario_name is None:
        return None, {}
    return scenario_name, get_scenario(scenario_name)


def _error_result(message: str) -> dict[str, Any]:
    return {
        "error": message,
        "suggested_actions": [],
        "agent_trace": [],
    }

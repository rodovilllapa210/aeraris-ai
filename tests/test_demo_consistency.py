"""Coherencia entre movimientos reales y outputs generados previamente."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

from demo.loader import (
    load_invoice_analysis,
    load_monthly_analysis,
    load_receipt_analysis,
    load_savings_plan,
    load_voice_analysis,
)
from processors.csv import analyze_transactions

TRANSACTIONS_DIR = Path("demo_data/transactions")


def test_monthly_output_matches_real_csv_calculation() -> None:
    calculated = analyze_transactions(
        TRANSACTIONS_DIR / "movimientos_septiembre.csv"
    )
    prepared = load_monthly_analysis()["deterministic_data"]

    assert prepared["income_eur"] == calculated.income
    assert prepared["expenses_eur"] == calculated.expenses
    assert prepared["savings_eur"] == calculated.savings
    assert prepared["savings_rate_pct"] == calculated.savings_rate


def test_document_and_voice_outputs_match_transactions() -> None:
    september = pd.read_csv(
        TRANSACTIONS_DIR / "movimientos_septiembre.csv",
        encoding="utf-8-sig",
    )
    electricity = september.loc[
        september["concepto"] == "Electricidad septiembre",
        "importe_eur",
    ].iloc[0]
    restaurant_ticket = september.loc[
        september["concepto"] == "Restaurante La Terraza",
        "importe_eur",
    ].iloc[0]

    invoice = load_invoice_analysis()
    receipt = load_receipt_analysis()
    voice = load_voice_analysis()["deterministic_data"]
    september_metrics = analyze_transactions(
        TRANSACTIONS_DIR / "movimientos_septiembre.csv"
    )
    july_metrics = analyze_transactions(
        TRANSACTIONS_DIR / "movimientos_julio.csv"
    )
    august_metrics = analyze_transactions(
        TRANSACTIONS_DIR / "movimientos_agosto.csv"
    )
    historical_average = round(
        (
            july_metrics.expenses_by_category["Restauracion"]
            + august_metrics.expenses_by_category["Restauracion"]
        )
        / 2,
        2,
    )

    assert invoice["data"]["total_eur"] == abs(electricity)
    assert receipt["data"]["total_eur"] == abs(restaurant_ticket)
    assert (
        voice["restaurant_spend_current_month_eur"]
        == september_metrics.expenses_by_category["Restauracion"]
    )
    assert voice["restaurant_spend_historical_average_eur"] == historical_average


def test_savings_plan_matches_three_month_calculation() -> None:
    monthly = [
        analyze_transactions(TRANSACTIONS_DIR / f"movimientos_{month}.csv")
        for month in ("julio", "agosto", "septiembre")
    ]
    plan = load_savings_plan()
    available = plan["inputs"]["available_savings_eur"]
    latest_savings = monthly[-1].savings
    target = round(sum(item.expenses for item in monthly) / 3 * 3)
    remaining = target - available

    assert plan["deterministic_results"]["target_eur"] == target
    assert plan["deterministic_results"]["remaining_eur"] == remaining
    assert plan["deterministic_results"]["estimated_months"] == math.ceil(
        remaining / latest_savings
    )

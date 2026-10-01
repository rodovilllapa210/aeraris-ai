"""Contratos compartidos entre la UI y los paquetes de trabajo."""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class InputType(str, Enum):
    TEXT = "text"
    PDF = "pdf"
    IMAGE = "image"
    CSV = "csv"
    AUDIO = "audio"


class AnalysisStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    ERROR = "error"


class WarningLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AnalysisRequest(BaseModel):
    input_type: InputType
    source_name: str | None = None
    file_path: str | None = None
    text: str | None = None
    question: str | None = None


class FinancialData(BaseModel):
    document_type: str | None = None
    supplier: str | None = None
    customer: str | None = None
    document_number: str | None = None
    date: datetime.date | None = None
    due_date: datetime.date | None = None
    currency: str = "EUR"
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    total_income: float | None = None
    total_expenses: float | None = None
    net_cash_flow: float | None = None
    categories: dict[str, float] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)


class AnalysisWarning(BaseModel):
    level: WarningLevel = WarningLevel.INFO
    code: str
    message: str


class ChartSpec(BaseModel):
    chart_type: str
    title: str
    labels: list[str] = Field(default_factory=list)
    values: list[float] = Field(default_factory=list)
    x: list[Any] = Field(default_factory=list)
    y: list[Any] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    status: AnalysisStatus = AnalysisStatus.SUCCESS
    input_type: InputType
    source_name: str | None = None
    extracted_text: str | None = None
    data: FinancialData = Field(default_factory=FinancialData)
    summary: str = ""
    warnings: list[AnalysisWarning] = Field(default_factory=list)
    suggested_questions: list[str] = Field(default_factory=list)
    charts: list[ChartSpec] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    question: str
    context: AnalysisResult


class ChatResponse(BaseModel):
    answer: str
    suggested_questions: list[str] = Field(default_factory=list)
    error: str | None = None


class TranscriptionResult(BaseModel):
    text: str
    language: str = "es"
    error: str | None = None


class SpeechResult(BaseModel):
    audio_path: str | None = None
    error: str | None = None

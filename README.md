# Aeraris AI

Copiloto financiero multimodal B2C.

## Objetivo

Aeraris ayuda a particulares a comprender documentos, movimientos, gastos y
conceptos financieros mediante una experiencia conversacional. La aplicación
combina entradas de documento, imagen, CSV, texto y voz con métricas, gráficos,
explicaciones y audio.

## Estado

Demo académica funcional desarrollada para el módulo de IA Generativa del Máster
en Inteligencia Artificial y Computación Cuántica Aplicada a los Mercados
Financieros del Instituto BME.

## Arquitectura agéntica y orquestada

La UI de Streamlit mantiene el contexto temporal de la conversación y delega cada
entrada al flujo adecuado:

UI conversacional
→ detección de intención o escenario
→ procesador especializado
→ cálculo determinista y/o output de modelo
→ respuesta, visualización y audio

Los contratos de core/schemas.py mantienen una frontera común entre interfaz,
orquestador, procesadores y modelos.

### Capacidades representadas

- Visión y documentos: extracción de información de facturas y tickets.
- Speech-to-text: transcripción de preguntas habladas.
- LLM: interpretación y explicación en lenguaje natural.
- Cálculo determinista: métricas financieras y simulaciones con Python.
- Gráficos: representación interactiva con Plotly.
- TTS: reproducción de un resumen mediante el WAV generado con Next-gen Kaldi.

## Qué se ejecuta en tiempo real

- Navegación y conversación.
- Carga y detección de archivos.
- Gestión del contexto de sesión.
- Lectura del CSV con pandas.
- Cálculo de ingresos, gastos, ahorro y tasa de ahorro.
- Agregación de gastos por categoría.
- Gráfico interactivo de categorías.
- Presentación de los cálculos del plan de ahorro.
- Reproducción del resumen de audio.

## Outputs generados previamente

Para que la presentación sea rápida y reproducible, los procesos de inferencia
pesada se ejecutaron previamente y sus resultados se conservan en
demo_data/outputs/:

- Análisis visual de facturas y tickets.
- Interpretación y explicación mediante LLM.
- Speech-to-text del escenario de voz.
- Generación TTS del resumen mensual.

Son resultados generados con modelos y reutilizados durante la demo para evitar
latencia, descargas de modelos y requisitos elevados de infraestructura. Los
cálculos numéricos del CSV y los gráficos sí se realizan durante la ejecución.

## Escenarios de demostración

- Factura eléctrica de septiembre.
- Ticket de restaurante en PDF o imagen.
- Movimientos bancarios de septiembre.
- Comparación por voz del gasto en restauración.
- Simulación educativa de un objetivo de ahorro.

## Instalación

Requiere Python 3.11 o posterior.

### Windows

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    run.bat

También puede iniciarse sin activar el entorno:

    .\.venv\Scripts\python.exe -m streamlit run streamlit_app.py

### Linux y macOS

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ./run.sh

La aplicación queda disponible normalmente en http://localhost:8501.

## Tests

    python -m pytest

Las pruebas cubren contratos, importaciones, carga de JSON, detección de
escenarios y cálculos financieros sobre el CSV real.

## Aviso

Aeraris ofrece herramientas de análisis y educación financiera. No proporciona
asesoramiento financiero personalizado.

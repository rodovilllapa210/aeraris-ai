# Aeraris AI

## Objetivo

Financial Copilot multimodal para PYMES.

## Estado

MVP académico en desarrollo.

## Modalidades previstas

- Texto
- PDF
- Imagen
- CSV
- Voz
- Audio de salida
- Visualizaciones

## Arquitectura

La interfaz de usuario envía todas las solicitudes al orquestador. Este selecciona los
procesadores y modelos adecuados, normaliza su salida mediante `AnalysisResult` y devuelve
el resultado a la interfaz:

`UI -> Orquestador -> procesadores/modelos -> AnalysisResult -> UI`

## Paquetes de trabajo

- WP1 UI/UX
- WP2 Document Intelligence
- WP3 AI Core / Orquestación
- WP4 Voz / Visualización / Infraestructura

## Instalación inicial

Requiere Python 3.11 o posterior.

### Windows

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
run.bat
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
./run.sh
```

## Tests

```bash
pytest
```

## Nota

El repositorio inicial contiene stubs y mocks para permitir el desarrollo paralelo.

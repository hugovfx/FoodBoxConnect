#!/usr/bin/env bash
# exit on error
set -o errexit

# Solo instalar dependencias
export PIP_DISABLE_PIP_VERSION_CHECK=1
pip install --no-cache-dir -r requirements.txt

# No ejecutar collectstatic, lo manejaremos en el código
echo "Skipping collectstatic, will handle static files in code"
#!/usr/bin/env bash
# exit on error
set -o errexit

# Suprimir avisos de pip
export PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalación de dependencias con output verboso para identificar problemas
pip install -r requirements.txt -v

# Mostrar las dependencias instaladas para verificar
pip list

# Recolectar archivos estáticos
python manage.py collectstatic --no-input --verbosity 2

# Imprimir mensaje de finalización para confirmar que el script terminó correctamente
echo "Build script completed successfully!"
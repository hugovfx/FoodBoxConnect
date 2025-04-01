#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalación de dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones (si usas una base de datos relacional, no sería necesario para MongoDB)
# python manage.py migrate
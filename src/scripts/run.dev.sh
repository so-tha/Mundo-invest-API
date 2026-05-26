#!/bin/bash

# Script para rodar em desenvolvimento

echo "Iniciando Mundo Invest API em modo desenvolvimento..."

# Ativar ambiente virtual (se existir)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Inicializar banco
python scripts/init_db.py

# Rodar servidor
uvicorn src.presentation.api.main:app --reload --host 0.0.0.0 --port 8000
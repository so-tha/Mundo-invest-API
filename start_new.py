#!/usr/bin/env python3
"""
Script simples de inicialização.
A aplicação FastAPI cuida do resto via lifespan events.
"""
import subprocess
import sys

if __name__ == "__main__":
    try:
        print("🚀 Iniciando Mundo Invest API...")
        subprocess.run([
            "uvicorn",
            "src.presentation.api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⚠️  Aplicação interrompida pelo usuário")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao iniciar aplicação: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}", file=sys.stderr)
        sys.exit(1)

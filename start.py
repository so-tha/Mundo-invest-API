#!/usr/bin/env python3
"""
Script de inicialização da aplicação.
"""
import asyncio
import subprocess
import sys
import time


async def wait_for_postgres(max_retries: int = 30) -> None: 
    for attempt in range(max_retries):
        try:
            import asyncpg
            conn = await asyncpg.connect(
                user='postgres',
                password='postgres',
                database='mundo_invest',
                host='db'
            )
            await conn.close()
            print(" PostgreSQL está pronto!")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                print(f" PostgreSQL não ficou pronto após {max_retries} tentativas", file=sys.stderr)
                raise
            print(f"   Tentativa {attempt + 1}/{max_retries}: aguardando... ({str(e)[:50]})")
            await asyncio.sleep(1)


async def initialize_database() -> None:
    try:
        from src.infrastructure.database.connection import init_db
        await init_db()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}", file=sys.stderr)
        sys.exit(1)


def start_application() -> None:
    subprocess.run([
        "uvicorn",
        "src.presentation.api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])


if __name__ == "__main__":
    try:
        asyncio.run(wait_for_postgres())
        asyncio.run(initialize_database())
        start_application()
    except KeyboardInterrupt:
        print("\n Aplicação interrompida pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n Erro fatal: {e}", file=sys.stderr)
        sys.exit(1)

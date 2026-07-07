import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


async def main():
    from src.infrastructure.database.connection import init_db

    print("Inicializando banco de dados...")
    await init_db()
    print("✓ Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())

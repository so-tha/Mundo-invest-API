import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.infrastructure.database.connection import init_db


async def main():
    print("Inicializando banco de dados...")
    await init_db()
    print("✓ Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
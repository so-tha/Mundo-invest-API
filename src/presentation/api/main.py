import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ...infrastructure.config.settings import settings
from .routes.clients import router as clientes_router
from .routes.webhooks import router as webhooks_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("📊 Inicializando banco de dados...")
    try:
        from tenacity import retry, stop_after_attempt, wait_exponential

        from ...infrastructure.database.connection import init_db

        @retry(
            stop=stop_after_attempt(10),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            reraise=True,
        )
        async def _init_with_retry():
            await init_db()

        await _init_with_retry()
        print("✅ Banco de dados inicializado!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        import traceback

        traceback.print_exc()

    yield

    print("👋 Encerrando aplicação...")


app = FastAPI(
    title="Mundo Invest API",
    description=(
        "Sistema de gerenciamento de clientes e patrimônios investidos, "
        "com integração ao Pipefy via GraphQL."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

_cors_origins = (
    ["*"]
    if settings.cors_origins == "*"
    else [o.strip() for o in settings.cors_origins.split(",")]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=_cors_origins != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(webhooks_router, prefix="/webhooks", tags=["Webhooks"])

_static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(_static_dir, "index.html"))


@app.get("/health")
async def health_check():
    try:
        from ...infrastructure.database.connection import engine

        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        return {
            "status": "ok",
            "service": "Mundo Invest API",
            "database": "✅ conectado",
        }
    except Exception as e:
        return {
            "status": "error",
            "service": "Mundo Invest API",
            "database": f"❌ {str(e)}",
        }

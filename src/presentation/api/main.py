from fastapi import FastAPI, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import asyncio
from .ui import get_ui_html
from .routes.clients import router as clientes_router
from .routes.webhooks import router as webhooks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await asyncio.sleep(3) 
        from ...infrastructure.database.connection import init_db
        await init_db()
    except Exception as e:
        logger.info(f"Erro ao inicializar banco: {e}")
        import traceback
        traceback.print_exc()
    yield
    logger.info("Encerrando aplicação.")


app = FastAPI(
    title="Mundo Invest API",
    description="Sistema de gerenciamento de clientes e patrimônios",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(webhooks_router, prefix="/webhooks", tags=["Webhooks"])

@app.get("/", response_class=HTMLResponse)
async def root():
    return get_ui_html()

@app.get("/health")
async def health_check():
    try:
        from ...infrastructure.database.connection import engine
        async with engine.connect() as conn:
            await conn.execute(__import__('sqlalchemy').text("SELECT 1"))
        return {
            "status": "ok",
            "service": "Mundo Invest API",
            "database": "✅ conectado"
        }
    except Exception as e:
        return {
            "status": "error",
            "service": "Mundo Invest API",
            "database": f"❌ {str(e)}"
        }
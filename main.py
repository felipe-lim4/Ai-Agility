from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from adapters.health import router as health_router
from adapters.readme_controller import router as readme_router
from infra.database.database import seed_default_tags
from infra.database.database import engine
from infra.database.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_default_tags()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_cache_frontend(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/frontend/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response



app.include_router(health_router)
app.include_router(readme_router)
# Servir arquivos estáticos do front-end
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Endpoint para renderizar o front principal
@app.get("/", response_class=FileResponse)
def render_front():
    return FileResponse("frontend/index.html")
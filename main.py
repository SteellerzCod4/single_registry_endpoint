from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from routers.auth import auth_router
from contextlib import asynccontextmanager
from db.database import init_db, close_db
from config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    # Инициализация базы данных при запуске
    await init_db()
    yield
    # Закрытие соединений при завершении
    await close_db()


app = FastAPI(lifespan=lifespan)

# Добавляем CORS middleware для работы с HTML формами
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # В продакшене укажите конкретные домены
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.include_router(auth_router)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/", response_class=FileResponse)
async def main_page():
    return FileResponse("static/main_page.html", media_type="text/html")


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=settings.server_host, 
        port=settings.server_port
    )
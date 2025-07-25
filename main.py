from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.auth import auth_router
from contextlib import asynccontextmanager
from db.database import init_db, close_db

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
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
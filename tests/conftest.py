pytest_plugins = ["pytest_asyncio"]
# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio 
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from main import app
from db import database as db_module          # db_module.Base, db_module.get_async_session

# ВАЖНО: импортируем модели, чтобы они зарегистрировали таблицы в metadata
from db import models     # тот модуль, где объявлен get_async_session


# ——— движок и sessionmaker для SQLite ———
TEST_DB_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DB_URL, echo=False, future=True)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

# ---------- event-loop для pytest-asyncio ----------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ---------- создаём таблицы один раз ----------
@pytest_asyncio.fixture(scope="session", autouse=True)   # <- меняем декоратор
async def _create_schema():
    async with test_engine.begin() as conn:
        await conn.run_sync(db_module.Base.metadata.create_all)
    yield
    await test_engine.dispose()

# ---------- override зависимости ----------
@pytest.fixture(scope="session")        # <= важно: session, чтобы отработал раньше client-фикстуры
def _override_async_session():
    async def _get_test_session() -> AsyncSession:
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[db_module.get_async_session] = _get_test_session
    yield
    app.dependency_overrides.clear()

# ---------- TestClient, зависит от override ----------
@pytest.fixture
def client(_override_async_session):    # <= явная зависимость гарантирует порядок
    with TestClient(app) as c:
        yield c

# ---- автоматическая очистка данных после каждого теста ----
@pytest_asyncio.fixture(autouse=True)
async def _clean_db_after_test():
    """
    После каждого теста удаляет все строки из всех таблиц, чтобы
    следующий тест начинал с чистой базы.
    """
    yield  # — здесь выполняется сам тест —

    async with TestSessionLocal() as session:
        # идём в обратном порядке, чтобы не споткнуться о FK-зависимостях
        for table in reversed(db_module.Base.metadata.sorted_tables):
            await session.execute(text(f'DELETE FROM "{table.name}"'))
        await session.commit()

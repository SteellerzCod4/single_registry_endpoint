from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from schemes.user import UserSignUp, UserResponse
from db.crud import create_user

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/registry", response_class=HTMLResponse)
async def registry_page():
    """Возвращает HTML страницу с формой регистрации"""
    try:
        with open("registration.html", "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Страница регистрации не найдена</h1>", status_code=404)


@auth_router.post("/registry", response_model=UserResponse)
async def registry(user_data: UserSignUp) -> UserResponse:
    user = await create_user(user_data)
    return user
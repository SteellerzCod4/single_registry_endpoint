from fastapi import APIRouter
from fastapi.responses import FileResponse
from schemes.user import UserSignUp, UserResponse
from db.crud import create_user

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/registry", response_class=FileResponse)
async def registry_page():
    """Возвращает HTML страницу с формой регистрации"""
    return FileResponse("templates/registration.html", media_type="text/html")


@auth_router.post("/registry", response_model=UserResponse)
async def registry(user_data: UserSignUp) -> UserResponse:
    user = await create_user(user_data)
    return user
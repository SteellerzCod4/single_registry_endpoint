from config import settings
from sqlalchemy import URL


url = URL.create(
    f"{settings.db_dialect}+{settings.db_api}",
    username=settings.user_name,
    password=settings.user_password,
    host=settings.host_name,
    port=settings.port,
    database=settings.db_name
)

if __name__ == "__main__":
    print(url)
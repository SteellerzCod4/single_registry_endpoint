import os
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()

url = URL.create(
    "+".join([os.getenv("DB_DIALECT"), os.getenv("DB_API")]),
    username=os.getenv("USER_NAME"),
    password=os.getenv("USER_PASSWORD"),
    host=os.getenv("HOST_NAME"),
    port=os.getenv("PORT"),
    database=os.getenv("DB_NAME")
)

if __name__ == "__main__":
    print(url)
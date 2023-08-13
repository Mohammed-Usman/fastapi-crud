from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user_name}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(
#             "host=localhost dbname=fastapi_crud user=postgres password=1234",
#             row_factory=dict_row)

#         cursor = conn.cursor()

#         print("DB SUccess")

#         break
#     except Exception as e:
#         print("DB connection failed")
#         print("Error", e)
#         time.sleep(2)

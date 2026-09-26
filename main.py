from fastapi import FastAPI
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker



class Settings(BaseSettings):
    database_url: str

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(
    title="Multi-Tenant Inventory & Order API",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "API is running!"
    }


@app.get("/health")
def health_check():
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from the project root
load_dotenv(dotenv_path=Path(".env"))

# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
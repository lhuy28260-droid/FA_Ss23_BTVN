from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Đọc file .env
load_dotenv()

# Lấy Database URL từ .env
DATABASE_URL = os.getenv("DATABASE_URL","mysql+pymysql://root:Soidenvip123%40@localhost:3306/secure_learning_portal.db")

# Tạo Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# Tạo Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base cho các Model
Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
# test_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Correct Database URL
DATABASE_URL = "mysql+mysqlconnector://aidrp_user:StrongPassword123!@localhost:3306/aidrp_db"

# ✅ Create SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    echo=True,        # Shows SQL in terminal for debugging
    pool_pre_ping=True
)

# ✅ Session Factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ✅ Base Class for ORM Models
Base = declarative_base()

# ✅ Test the Connection
try:
    with engine.connect() as conn:
        print("✅ SQLAlchemy connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)

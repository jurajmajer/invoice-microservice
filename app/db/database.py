import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.getenv('DB_URI'), pool_recycle=3600, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

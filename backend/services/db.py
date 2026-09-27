from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine=create_engine("sqlite:///user_db")
SessionLocal=sessionmaker(bind=engine)

from fastapi import Depends
from sqlalchemy.orm import Session
from  services.model import User, ChatMessage, Base 
from services.db import engine, SessionLocal
from core.security import get_password_hash
from schemas.models import UserCreate
Base.metadata.create_all(bind=engine)



def create_user(user:UserCreate,db:Session):
    hashed_pass=get_password_hash(user.password)
    db_user = User(username=user.username,hashed_password=hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db:Session,username:str):
    return db.query(User).filter(User.username==username).first()

def create_chat_message(db:Session,user_id:int,human_message:str,ai_message:str):
    obj=ChatMessage(user_id=user_id,human_message=human_message,ai_message=ai_message)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_chat_history(db:Session,user_id:int):
    obj= db.query(ChatMessage).filter(ChatMessage.user_id==user_id).all()
    return obj



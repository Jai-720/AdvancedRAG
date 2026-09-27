from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,autoincrement="auto")
    username=Column(String(50),unique=True,nullable=False)
    hashed_password:Mapped[str]=mapped_column(unique=True)



class ChatMessage(Base):
    __tablename__="chat_messages"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    human_message=Column(String)
    ai_message=Column(String)

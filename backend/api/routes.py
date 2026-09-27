from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from schemas.models import ChatRequest, ChatResponse ,UserCreate
from core.rag_engine import generate_response
from services.db import SessionLocal
from services.crud import create_user,get_user_by_username,create_chat_message,get_chat_history
from sqlalchemy.orm import Session
from core.security import verify_password,create_access_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import jwt
import shutil
from pathlib import Path
from core.ingestion import process_document
from dotenv import load_dotenv
import os

router = APIRouter()

def getdb():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, str(os.getenv("JWT_SECRET_KEY")), algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return int(user_id)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(getdb), user_id: int = Depends(get_current_user)):
    user_text = request.user_input
    history = get_chat_history(db=db, user_id=user_id)

    formatted_history = ""
    for item in history:
        formatted_history += f"Ai message:{item.ai_message},\nHuman msg:{item.human_message}\n"

    ai_answer = generate_response(user_text, formatted_history,user_id)

    create_chat_message(db=db, user_id=user_id, human_message=user_text, ai_message=ai_answer)
    return ChatResponse(answer=ai_answer)

@router.post("/signup")
def Signup(user:UserCreate,db:Session=Depends(getdb)):
    if get_user_by_username(db,user.username):
       raise HTTPException(status_code=400,detail="User=name already registered")

    create_user(user,db)
    return {"message": "Successfully signed up"}



@router.post("/login")
def Login(user:UserCreate,db:Session=Depends(getdb)):
   db_user=get_user_by_username(db=db,username=user.username)
   if (not db_user):
      raise HTTPException(status_code=400 ,detail="Invalid credentials")
   elif( not verify_password(hashed_password=db_user.hashed_password,plain_password=user.password)):
      raise HTTPException(status_code=400, detail="Invalid Credentials")
   token=create_access_token(data={"sub":str(db_user.id)})
   return {"access_token":token,"token_type":"bearer"}


@router.post("/upload")
def pdfdocs(file: UploadFile = File(...),
            current_user:str=Depends(get_current_user)):
    upload_dir = Path(__file__).resolve().parent.parent / f"temp_uploads/{current_user}"

    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{file.filename}"
    if file_path.exists():
        return {"message":"File Already Processed and available for chat"}

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_document(str(file_path),current_user)
    return {"message":"success"}
        
    

      
    
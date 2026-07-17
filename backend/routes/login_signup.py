from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm
import models
from datetime import datetime
from schemas.user_schemas import UserCreate
from auth.jwt_auth import verify_password,create_access_token,hash_password

router=APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token=create_access_token({"user_id":user.user_id})
    return {"access_token":token,"token_type":"bearer","role":user.role}
        
@router.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(
        models.User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(data.password)

    user = models.User(
        email=data.email,
        hashed_password=hashed_password,
        role=data.role,
        is_active=1,
        created_at=datetime.now()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}
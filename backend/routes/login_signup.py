from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.user_schemas import UserCreate
from auth.jwt_auth import verify_password,create_access_token

router=APIRouter()

@router.post("/login")
def login(email:str,password:str,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==email).first()
    if not user or not verify_password(password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token=create_access_token({"user_id":user.user_id})
    return {"access_token":token,"token_type":"bearer"}
        
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
        password=hashed_password,
        role=data.role,
        phone=data.phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}
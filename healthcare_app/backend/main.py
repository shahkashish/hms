from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Healthcare Management System", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class User(BaseModel):
    email: str
    password: str
    full_name: str
    role: str
    tenant_id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    tenant_id: Optional[str] = None

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(user: User):
    response = supabase.auth.sign_in_with_password({
        "email": user.email,
        "password": user.password
    })
    if response.error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": response.session.access_token, "token_type": "bearer"}

@app.post("/register")
async def register(user: User):
    response = supabase.auth.sign_up({
        "email": user.email,
        "password": user.password,
        "options": {"data": {"full_name": user.full_name, "role": user.role, "tenant_id": user.tenant_id}}
    })
    if response.error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.error.message
        )
    return {"message": "User registered successfully"}

@app.get("/patients")
async def get_patients(token: str = Depends(oauth2_scheme)):
    try:
        response = supabase.auth.get_user(token)
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        patients = supabase.table("patients").select("*").execute()
        return patients.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )(token: str = Depends(oauth2_scheme)):
    try:
        # Verify token
        response = supabase.auth.get_user(token)
        if response.error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get patients from Supabase
        patients = supabase.table("patients").select("*").execute()
        return patients.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
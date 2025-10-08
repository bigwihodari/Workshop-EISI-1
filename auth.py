from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from . import models, schemas, database


# LES VARIABLES D'ENVIRONNEMENT

load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter(tags=["Authentification"])



# hachage et vérification

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



# GESTION DES TOKENS

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Décoder et vérifier le token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")



# UTILITAIRES UTILISATEUR

def get_user_by_username(db: Session, username: str):
    return db.query(models.Joueurs).filter(models.Joueurs.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    username = verify_token(token)
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user



# ROUTES D'AUTHENTIFICATION

@router.post("/signup", response_model=schemas.JoueurResponse)
def signup(joueur: schemas.JoueurCreate, db: Session = Depends(database.SessionLocal)):
    """Créer un nouveau joueur"""
    existing_user = db.query(models.Joueurs).filter(models.Joueurs.username == joueur.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    hashed_pwd = get_password_hash(joueur.password)
    new_user = models.Joueurs(
        username=joueur.username,
        email=joueur.email,
        password=hashed_pwd,
        score=0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    """Connexion et génération du JWT"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.JoueurResponse)
def read_users_me(current_user: schemas.JoueurResponse = Depends(get_current_user)):
    """Route protégée : récupérer les infos du joueur connecté"""
    return current_user

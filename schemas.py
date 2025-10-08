from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from datetime import datetime


# Salles
class SalleBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ordre: Optional[int] = None


class SalleCreate(SalleBase):
    pass


class SalleResponse(SalleBase):
    id_salle: int

    class Config:
        orm_mode = True


# Enigmes
class EnigmeBase(BaseModel):
    name: str
    description: Optional[str] = None
    type_enigme: Optional[str] = None
    indice: Optional[str] = None
    id_salle: int


class EnigmeCreate(EnigmeBase):
    pass


class EnigmeResponse(EnigmeBase):
    id_enigme: int

    class Config:
        orm_mode = True


# Medicaments
class MedicamentBase(BaseModel):
    name: str
    composition_1: Optional[str] = None
    composition_2: Optional[str] = None
    composition_3: Optional[str] = None


class MedicamentCreate(MedicamentBase):
    pass


class MedicamentResponse(MedicamentBase):
    id_medoc: int

    class Config:
        orm_mode = True


# Maladies
class MaladieBase(BaseModel):
    name: str
    symptome_1: Optional[str] = None
    symptome_2: Optional[str] = None
    symptome_3: Optional[str] = None
    symptome_4: Optional[str] = None
    symptome_5: Optional[str] = None
    frequence_medoc: Optional[int] = None
    id_medoc: int


class MaladieCreate(MaladieBase):
    pass


class MaladieResponse(MaladieBase):
    id_mal: int

    class Config:
        orm_mode = True


# Partie
class PartieBase(BaseModel):
    nombre_joueurs: Optional[int] = None
    etat_sante: Optional[str] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    temps_restant: Optional[int] = None
    temperature: Optional[float] = None


class PartieCreate(PartieBase):
    pass


class PartieResponse(PartieBase):
    id_game: int

    class Config:
        orm_mode = True


# Joueurs
class JoueurBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None


class JoueurCreate(JoueurBase):
    password: str


class JoueurResponse(JoueurBase):
    id_joueur: int
    score: Optional[int] = None
    id_game: Optional[int] = None

    class Config:
        orm_mode = True


# Reponses
class ReponseBase(BaseModel):
    reponse_saisie: Optional[str] = None
    date_reponse: Optional[date] = None
    correcte: Optional[bool] = None
    id_salle: int
    id_joueur: int


class ReponseCreate(ReponseBase):
    pass


class ReponseResponse(ReponseBase):
    id_resp: int

    class Config:
        orm_mode = True


# Token (auth)
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

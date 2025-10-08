from sqlalchemy import Column, Integer, String, Date, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Salles(Base):
    __tablename__ = "salles"

    id_salle = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    description = Column(String(250), nullable=True)
    ordre = Column(Integer, nullable=True)
    enigmes = relationship("Enigme", back_populates="salle")
    responses = relationship("Responses", back_populates="salle")


class Enigme(Base):
    __tablename__ = "enigme"

    id_enigme = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=True)
    type_enigme = Column(String(50), nullable=True)
    indice = Column(String(50), nullable=True)
    id_salle = Column(Integer, ForeignKey("salles.id_salle"), nullable=False)
    salle = relationship("salles", back_populates="enigmes")



class Medicaments(Base):
    __tablename__ = "medicaments"

    id_medoc = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    composition_1 = Column(String(50), nullable=True)
    composition_2 = Column(String(50), nullable=True)
    composition_3 = Column(String(50), nullable=True)
    maladie = relationship("Maladies", back_populates="medicament", uselist=False)


class Maladies(Base):
    __tablename__ = "maladies"

    id_mal = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    symptome_1 = Column(String(50), nullable=True)
    symptome_2 = Column(String(50), nullable=True)
    symptome_3 = Column(String(50), nullable=True)
    symptome_4 = Column(String(50), nullable=True)
    symptome_5 = Column(String(50), nullable=True)
    frequence_medoc = Column(Integer, nullable=True)

    id_medoc = Column(Integer, ForeignKey("medicaments.id_medoc"), nullable=False, unique=True)

    medicament = relationship("Medicaments", back_populates="maladie")



class Partie(Base):
    __tablename__ = "partie"

    id_game = Column(Integer, primary_key=True, index=True)
    nombre_joueurs = Column(Integer, nullable=True)
    etat_sante = Column(String(50), nullable=True)
    date_debut = Column(Date, nullable=True)
    date_fin = Column(Date, nullable=True)
    temps_restant = Column(Integer, nullable=True)
    temperature = Column(DECIMAL(15, 2), nullable=True)
    joueurs = relationship("Joueurs", back_populates="partie")

    


class Joueurs(Base):
    __tablename__ = "joueurs"

    id_joueur = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True)
    password = Column(String(50), nullable=False)
    score = Column(Integer, nullable=True)
    id_game = Column(Integer, ForeignKey("partie.id_partie"), nullable=True)
    partie = relationship("Partie", back_populates="joueurs")
    responses = relationship("Responses", back_populates="joueur")
    

class Responses(Base):
    __tablename__ = "responses"

    id_resp = Column(Integer, primary_key=True, index=True)
    reponse_saisie = Column(String(50), nullable=True)
    date_reponse = Column(Date, nullable=True)
    correcte = Column(Boolean, nullable=True)

    id_salle = Column(Integer, ForeignKey("salles.id_salle"), nullable=False)
    id_joueur = Column(Integer, ForeignKey("joueurs.id_joueur"), nullable=False)

    salle = relationship("Salles", back_populates="reponses")
    joueur = relationship("Joueurs", back_populates="reponses")

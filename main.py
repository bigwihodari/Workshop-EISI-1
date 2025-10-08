from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database, auth

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Escape Game API", version="1.0")

# Inclusion du router d'authentification (signup, login, me)
app.include_router(auth.router)



# DÉPENDANCE BASE DE DONNÉES

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



# SALLES

@app.get("/salles", response_model=List[schemas.SalleResponse])
def get_salles(db: Session = Depends(get_db)):
    return db.query(models.Salles).all()


@app.get("/salles/{id}", response_model=schemas.SalleResponse)
def get_salle(id: int, db: Session = Depends(get_db)):
    salle = db.query(models.Salles).filter(models.Salles.id_salle == id).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle introuvable")
    return salle


@app.post("/salles", response_model=schemas.SalleResponse)
def create_salle(salle: schemas.SalleCreate, db: Session = Depends(get_db),
                 current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_salle = models.Salles(**salle.dict())
    db.add(new_salle)
    db.commit()
    db.refresh(new_salle)
    return new_salle


@app.put("/salles/{id}", response_model=schemas.SalleResponse)
def update_salle(id: int, updated: schemas.SalleCreate, db: Session = Depends(get_db),
                 current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    salle = db.query(models.Salles).filter(models.Salles.id_salle == id).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    for k, v in updated.dict().items():
        setattr(salle, k, v)
    db.commit()
    db.refresh(salle)
    return salle


@app.delete("/salles/{id}")
def delete_salle(id: int, db: Session = Depends(get_db),
                 current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    salle = db.query(models.Salles).filter(models.Salles.id_salle == id).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle introuvable")
    db.delete(salle)
    db.commit()
    return {"message": "Salle supprimée"}



# ENIGMES

@app.get("/enigmes", response_model=List[schemas.EnigmeResponse])
def get_enigmes(db: Session = Depends(get_db)):
    return db.query(models.Enigme).all()


@app.post("/enigmes", response_model=schemas.EnigmeResponse)
def create_enigme(enigme: schemas.EnigmeCreate, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_enigme = models.Enigme(**enigme.dict())
    db.add(new_enigme)
    db.commit()
    db.refresh(new_enigme)
    return new_enigme


@app.put("/enigmes/{id}", response_model=schemas.EnigmeResponse)
def update_enigme(id: int, updated: schemas.EnigmeCreate, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    enigme = db.query(models.Enigme).filter(models.Enigme.id_enigme == id).first()
    if not enigme:
        raise HTTPException(status_code=404, detail="Enigme non trouvée")
    for k, v in updated.dict().items():
        setattr(enigme, k, v)
    db.commit()
    db.refresh(enigme)
    return enigme


@app.delete("/enigmes/{id}")
def delete_enigme(id: int, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    enigme = db.query(models.Enigme).filter(models.Enigme.id_enigme == id).first()
    if not enigme:
        raise HTTPException(status_code=404, detail="Enigme introuvable")
    db.delete(enigme)
    db.commit()
    return {"message": "Enigme supprimée"}



# MEDICAMENTS 

@app.get("/medicaments", response_model=List[schemas.MedicamentResponse])
def get_medicaments(db: Session = Depends(get_db)):
    return db.query(models.Medicaments).all()


@app.post("/medicaments", response_model=schemas.MedicamentResponse)
def create_medicament(medoc: schemas.MedicamentCreate, db: Session = Depends(get_db),
                      current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_medoc = models.Medicaments(**medoc.dict())
    db.add(new_medoc)
    db.commit()
    db.refresh(new_medoc)
    return new_medoc


@app.put("/medicaments/{id}", response_model=schemas.MedicamentResponse)
def update_medicament(id: int, updated: schemas.MedicamentCreate, db: Session = Depends(get_db),
                      current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    medoc = db.query(models.Medicaments).filter(models.Medicaments.id_medoc == id).first()
    if not medoc:
        raise HTTPException(status_code=404, detail="Médicament introuvable")
    for k, v in updated.dict().items():
        setattr(medoc, k, v)
    db.commit()
    db.refresh(medoc)
    return medoc


@app.delete("/medicaments/{id}")
def delete_medicament(id: int, db: Session = Depends(get_db),
                      current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    medoc = db.query(models.Medicaments).filter(models.Medicaments.id_medoc == id).first()
    if not medoc:
        raise HTTPException(status_code=404, detail="Médicament introuvable")
    db.delete(medoc)
    db.commit()
    return {"message": "Médicament supprimé"}



# MALADIES 

@app.get("/maladies", response_model=List[schemas.MaladieResponse])
def get_maladies(db: Session = Depends(get_db)):
    return db.query(models.Maladies).all()


@app.post("/maladies", response_model=schemas.MaladieResponse)
def create_maladie(maladie: schemas.MaladieCreate, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_maladie = models.Maladies(**maladie.dict())
    db.add(new_maladie)
    db.commit()
    db.refresh(new_maladie)
    return new_maladie


@app.put("/maladies/{id}", response_model=schemas.MaladieResponse)
def update_maladie(id: int, updated: schemas.MaladieCreate, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    maladie = db.query(models.Maladies).filter(models.Maladies.id_mal == id).first()
    if not maladie:
        raise HTTPException(status_code=404, detail="Maladie introuvable")
    for k, v in updated.dict().items():
        setattr(maladie, k, v)
    db.commit()
    db.refresh(maladie)
    return maladie


@app.delete("/maladies/{id}")
def delete_maladie(id: int, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    maladie = db.query(models.Maladies).filter(models.Maladies.id_mal == id).first()
    if not maladie:
        raise HTTPException(status_code=404, detail="Maladie introuvable")
    db.delete(maladie)
    db.commit()
    return {"message": "Maladie supprimée"}



# PARTIE

@app.get("/parties", response_model=List[schemas.PartieResponse])
def get_parties(db: Session = Depends(get_db)):
    return db.query(models.Partie).all()


@app.post("/parties", response_model=schemas.PartieResponse)
def create_partie(partie: schemas.PartieCreate, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_partie = models.Partie(**partie.dict())
    db.add(new_partie)
    db.commit()
    db.refresh(new_partie)
    return new_partie


@app.put("/parties/{id}", response_model=schemas.PartieResponse)
def update_partie(id: int, updated: schemas.PartieCreate, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    partie = db.query(models.Partie).filter(models.Partie.id_game == id).first()
    if not partie:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    for k, v in updated.dict().items():
        setattr(partie, k, v)
    db.commit()
    db.refresh(partie)
    return partie


@app.delete("/parties/{id}")
def delete_partie(id: int, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    partie = db.query(models.Partie).filter(models.Partie.id_game == id).first()
    if not partie:
        raise HTTPException(status_code=404, detail="Partie introuvable")
    db.delete(partie)
    db.commit()
    return {"message": "Partie supprimée"}



# JOUEURS 

@app.get("/joueurs", response_model=List[schemas.JoueurResponse])
def get_joueurs(db: Session = Depends(get_db)):
    return db.query(models.Joueurs).all()


@app.get("/joueurs/{id}", response_model=schemas.JoueurResponse)
def get_joueur(id: int, db: Session = Depends(get_db)):
    joueur = db.query(models.Joueurs).filter(models.Joueurs.id_joueur == id).first()
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur introuvable")
    return joueur


@app.delete("/joueurs/{id}")
def delete_joueur(id: int, db: Session = Depends(get_db),
                  current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    joueur = db.query(models.Joueurs).filter(models.Joueurs.id_joueur == id).first()
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur introuvable")
    db.delete(joueur)
    db.commit()
    return {"message": "Joueur supprimé"}



# REPONSES

@app.get("/reponses", response_model=List[schemas.ReponseResponse])
def get_reponses(db: Session = Depends(get_db)):
    return db.query(models.Responses).all()


@app.post("/reponses", response_model=schemas.ReponseResponse)
def create_reponse(resp: schemas.ReponseCreate, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    new_resp = models.Responses(**resp.dict())
    db.add(new_resp)
    db.commit()
    db.refresh(new_resp)
    return new_resp


@app.put("/reponses/{id}", response_model=schemas.ReponseResponse)
def update_reponse(id: int, updated: schemas.ReponseCreate, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    resp = db.query(models.Responses).filter(models.Responses.id_resp == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Réponse introuvable")
    for k, v in updated.dict().items():
        setattr(resp, k, v)
    db.commit()
    db.refresh(resp)
    return resp


@app.delete("/reponses/{id}")
def delete_reponse(id: int, db: Session = Depends(get_db),
                   current_user: schemas.JoueurResponse = Depends(auth.get_current_user)):
    resp = db.query(models.Responses).filter(models.Responses.id_resp == id).first()
    if not resp:
        raise HTTPException(status_code=404, detail="Réponse introuvable")
    db.delete(resp)
    db.commit()
    return {"message": "Réponse supprimée"}

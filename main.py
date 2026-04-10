from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

import models, schemas, crud
from database import engine, get_db

# Create the database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Farm Management API (FastAPI)",
    description="API for managing kandang, lantai, actuators, and configs. Automatically generates Swagger UI.",
    version="1.0.0"
)

# --- Kandang Routes ---
@app.get("/api/kandang", response_model=List[schemas.Kandang], tags=["Kandang"])
def read_kandangs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_kandangs(db, skip=skip, limit=limit)

@app.post("/api/kandang", response_model=schemas.Kandang, status_code=201, tags=["Kandang"])
def create_kandang(kandang: schemas.KandangCreate, db: Session = Depends(get_db)):
    return crud.create_kandang(db=db, kandang=kandang)

# --- Lantai Routes ---
@app.get("/api/lantai", response_model=List[schemas.Lantai], tags=["Lantai"])
def read_lantais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_lantais(db, skip=skip, limit=limit)

@app.post("/api/lantai", response_model=schemas.Lantai, status_code=201, tags=["Lantai"])
def create_lantai(lantai: schemas.LantaiCreate, db: Session = Depends(get_db)):
    return crud.create_lantai(db=db, lantai=lantai)

# --- Actuator Routes ---
@app.get("/api/actuators", response_model=List[schemas.Actuator], tags=["Actuators"])
def read_actuators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_actuators(db, skip=skip, limit=limit)

@app.post("/api/actuators", response_model=schemas.Actuator, status_code=201, tags=["Actuators"])
def create_actuator(actuator: schemas.ActuatorCreate, db: Session = Depends(get_db)):
    return crud.create_actuator(db=db, actuator=actuator)

# --- Config Routes ---
@app.get("/api/actuators/{uuid}/blower_config", response_model=schemas.BlowerConfig, tags=["Config"])
def get_blower_config(uuid: UUID, db: Session = Depends(get_db)):
    config = crud.get_blower_config(db, actuator_id=uuid)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config

@app.put("/api/actuators/{uuid}/blower_config", response_model=schemas.BlowerConfig, tags=["Config"])
def update_blower_config(uuid: UUID, config: schemas.BlowerConfigCreate, db: Session = Depends(get_db)):
    return crud.update_blower_config(db, actuator_id=uuid, config=config)

# Note: In a full production implementation, you would write similar 
# routes here for dimmer_config, heater_config, and pump_config.

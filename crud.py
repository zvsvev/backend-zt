from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas

# Kandang
def get_kandangs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kandang).offset(skip).limit(limit).all()

def create_kandang(db: Session, kandang: schemas.KandangCreate):
    db_obj = models.Kandang(**kandang.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Lantai
def get_lantais(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lantai).offset(skip).limit(limit).all()

def create_lantai(db: Session, lantai: schemas.LantaiCreate):
    db_obj = models.Lantai(**lantai.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Actuator
def get_actuators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Actuator).offset(skip).limit(limit).all()

def create_actuator(db: Session, actuator: schemas.ActuatorCreate):
    db_obj = models.Actuator(**actuator.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# Configs (Example for Blower)
def get_blower_config(db: Session, actuator_id: UUID):
    return db.query(models.BlowerConfig).filter(models.BlowerConfig.actuator_id == actuator_id).first()

def update_blower_config(db: Session, actuator_id: UUID, config: schemas.BlowerConfigCreate):
    db_obj = db.query(models.BlowerConfig).filter(models.BlowerConfig.actuator_id == actuator_id).first()
    if db_obj:
        for key, value in config.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)
    else:
        db_obj = models.BlowerConfig(actuator_id=actuator_id, **config.model_dump())
        db.add(db_obj)
    
    # Normally, you would emit a ConfigAuditLog here!
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

# We will skip writing out every single dimmer/heater/pump crud to save space,
# they can be easily duplicated or accessed directly in main.py logic!

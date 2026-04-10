import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Kandang(Base):
    __tablename__ = "kandang"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    lokasi = Column(String)

    lantais = relationship("Lantai", back_populates="kandang", cascade="all, delete-orphan")


class Lantai(Base):
    __tablename__ = "lantai"

    id = Column(Integer, primary_key=True, index=True)
    kandang_id = Column(Integer, ForeignKey("kandang.id"))
    name = Column(String, index=True)

    kandang = relationship("Kandang", back_populates="lantais")
    actuators = relationship("Actuator", back_populates="lantai", cascade="all, delete-orphan")


class Actuator(Base):
    __tablename__ = "actuator"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lantai_id = Column(Integer, ForeignKey("lantai.id"))
    name = Column(String, index=True)
    type = Column(String) # blower, dimmer, heater, pump
    mode = Column(String)
    current_status = Column(Boolean, default=False)
    current_value = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lantai = relationship("Lantai", back_populates="actuators")

    blower_config = relationship("BlowerConfig", back_populates="actuator", uselist=False, cascade="all, delete-orphan")
    dimmer_config = relationship("DimmerConfig", back_populates="actuator", uselist=False, cascade="all, delete-orphan")
    heater_config = relationship("HeaterConfig", back_populates="actuator", uselist=False, cascade="all, delete-orphan")
    pump_config = relationship("PumpConfig", back_populates="actuator", uselist=False, cascade="all, delete-orphan")


class BlowerConfig(Base):
    __tablename__ = "blower_config"

    actuator_id = Column(UUID(as_uuid=True), ForeignKey("actuator.uuid"), primary_key=True)
    interval_on_duration = Column(Integer)
    interval_off_duration = Column(Integer)
    min_temperature = Column(Float)
    max_temperature = Column(Float)

    actuator = relationship("Actuator", back_populates="blower_config")


class DimmerConfig(Base):
    __tablename__ = "dimmer_config"

    actuator_id = Column(UUID(as_uuid=True), ForeignKey("actuator.uuid"), primary_key=True)
    min_brightness = Column(Integer)
    max_brightness = Column(Integer)

    actuator = relationship("Actuator", back_populates="dimmer_config")


class HeaterConfig(Base):
    __tablename__ = "heater_config"

    actuator_id = Column(UUID(as_uuid=True), ForeignKey("actuator.uuid"), primary_key=True)
    min_temperature = Column(Float)
    max_temperature = Column(Float)

    actuator = relationship("Actuator", back_populates="heater_config")


class PumpConfig(Base):
    __tablename__ = "pump_config"

    actuator_id = Column(UUID(as_uuid=True), ForeignKey("actuator.uuid"), primary_key=True)
    interval_on_duration = Column(Integer)
    interval_off_duration = Column(Integer)

    actuator = relationship("Actuator", back_populates="pump_config")


class ConfigAuditLog(Base):
    __tablename__ = "config_audit_log"

    id_log = Column(Integer, primary_key=True, index=True)
    actuator_id = Column(UUID(as_uuid=True))
    parameter_yang_diubah = Column(String)
    nilai_lama = Column(String)
    nilai_baru = Column(String)
    waktu_perubahan = Column(DateTime, default=datetime.utcnow)

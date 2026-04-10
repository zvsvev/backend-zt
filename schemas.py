from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# --- Kandang ---
class KandangBase(BaseModel):
    name: str
    lokasi: str

class KandangCreate(KandangBase):
    pass

class Kandang(KandangBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Lantai ---
class LantaiBase(BaseModel):
    name: str
    kandang_id: int

class LantaiCreate(LantaiBase):
    pass

class Lantai(LantaiBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# --- Actuator ---
class ActuatorBase(BaseModel):
    name: str
    type: str # blower, dimmer, heater, pump
    mode: str
    lantai_id: int
    current_status: bool = False
    current_value: float = 0.0

class ActuatorCreate(ActuatorBase):
    pass

class Actuator(ActuatorBase):
    uuid: UUID
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# --- Configs ---
class BlowerConfigBase(BaseModel):
    interval_on_duration: Optional[int] = None
    interval_off_duration: Optional[int] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None

class BlowerConfigCreate(BlowerConfigBase):
    pass

class BlowerConfig(BlowerConfigBase):
    actuator_id: UUID
    model_config = ConfigDict(from_attributes=True)


class DimmerConfigBase(BaseModel):
    min_brightness: Optional[int] = None
    max_brightness: Optional[int] = None

class DimmerConfigCreate(DimmerConfigBase):
    pass

class DimmerConfig(DimmerConfigBase):
    actuator_id: UUID
    model_config = ConfigDict(from_attributes=True)


class HeaterConfigBase(BaseModel):
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None

class HeaterConfigCreate(HeaterConfigBase):
    pass

class HeaterConfig(HeaterConfigBase):
    actuator_id: UUID
    model_config = ConfigDict(from_attributes=True)


class PumpConfigBase(BaseModel):
    interval_on_duration: Optional[int] = None
    interval_off_duration: Optional[int] = None

class PumpConfigCreate(PumpConfigBase):
    pass

class PumpConfig(PumpConfigBase):
    actuator_id: UUID
    model_config = ConfigDict(from_attributes=True)


# --- Audit Logs ---
class ConfigAuditLog(BaseModel):
    id_log: int
    actuator_id: UUID
    parameter_yang_diubah: str
    nilai_lama: str
    nilai_baru: str
    waktu_perubahan: datetime
    model_config = ConfigDict(from_attributes=True)

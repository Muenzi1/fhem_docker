from pydantic import BaseModel


class DeviceBase(BaseModel):
    pass


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    id: int
    device: str
    display_name: str
    dashboard: str

    class Config:
        orm_mode = True


class ReadingBase(BaseModel):
    pass


class ReadingCreate(ReadingBase):
    pass


class Reading(ReadingBase):
    id: int
    reading: str
    unit: str

    class Config:
        orm_mode = True


class ClimateBase(BaseModel):
    pass


class ClimateCreate(ClimateBase):
    pass


class Climate(ClimateBase):
    id: int
    devices: Device
    readings: Reading
    value: float

    class Config:
        orm_mode = True

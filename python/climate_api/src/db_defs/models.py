from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base


class Devices(Base):
    __tablename__ = "d_t_device_mapping"

    id = Column(Integer, primary_key=True, index=True)
    device = Column(String, unique=True)
    display_name = Column(String)
    type = Column(String)
    dashboard = Column(String)
    _created_at = Column(DateTime)

    room_climates = relationship("Climate", back_populates="devices")


class Readings(Base):
    __tablename__ = "d_t_reading_mapping"

    id = Column(Integer, primary_key=True, index=True)
    reading_orig = Column(String, unique=True)
    reading = Column(String)
    unit = Column(String)
    _created_at = Column(DateTime)

    room_climates = relationship("Climate", back_populates="readings")


class Climate(Base):
    __tablename__ = "f_t_climate"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    year = Column(Integer)
    month = Column(Integer)
    week = Column(Integer)
    day = Column(Integer)
    fk_device_id = Column(Integer, ForeignKey("d_t_device_mapping.id"))
    fk_reading_id = Column(Integer, ForeignKey("d_t_reading_mapping.id"))
    value = Column(Float)
    _created_at = Column(DateTime)

    devices = relationship("Devices", back_populates="room_climates")
    readings = relationship("Readings", back_populates="room_climates")

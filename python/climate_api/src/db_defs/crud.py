from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models

# from . import schemas


def get_measurement_by_device_id(db: Session, device_id: int, limit=100):
    max_ids_per_device_reading = (
        db.query(func.max(models.Climate.id))
        .filter(models.Climate.fk_device_id == device_id)
        .group_by(models.Climate.fk_reading_id)
        .subquery()
    )

    recent_measurement = (
        db.query(models.Climate)
        .join(
            max_ids_per_device_reading,
            models.Climate.id == max_ids_per_device_reading.c.max,
        )
        .limit(limit)
        .all()
    )

    return recent_measurement


def get_climate_devices(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Devices)
        .where(models.Devices.display_name.endswith("_Raum"))
        .offset(skip)
        .limit(limit)
        .all()
    )

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from db_defs import crud, models, schemas, database

# from db_defs.database import SessionDb, engine

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionDb()
    try:
        yield db
    finally:
        db.close()


@app.get("/devices/", response_model=list[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_climate_devices(db, skip=skip, limit=limit)
    return devices


@app.get("/climate/{device_id}", response_model=list[schemas.Climate])
def read_climate_per_device(device_id: int, db: Session = Depends(get_db)):
    climate = crud.get_measurement_by_device_id(db, device_id)
    return climate


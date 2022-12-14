import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("hostname")
PORT = os.getenv("mariadb_port")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/fhem?charset=utf8mb4"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionDb = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

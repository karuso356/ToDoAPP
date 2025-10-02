from sqlmodel import SQLModel, Session
from sqlmodel import create_engine
from typing import Annotated
from fastapi import Depends, FastAPI

# Datos de conexión (ajusta según tu RDS)
DB_USER = "admin1"          # tu usuario de RDS
DB_PASSWORD = "Elefante123" # tu contraseña de RDS
DB_NAME = "database1"      # nombre de la base de datos creada en RDS
DB_HOST = "database1.cn62i4ik22wg.us-east-2.rds.amazonaws.com"
DB_PORT = "5432"           # 5432 para PostgreSQL, 3306 si usas MySQL

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crea el engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]




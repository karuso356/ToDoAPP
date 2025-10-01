from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, select
from typing import Optional, List
from db import engine, create_db_and_tables, SessionDep 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Aplicacion para administrar tus actividades :)"}


@app.get("/check-db")
def check_db(session:SessionDep):
    result = session.exec(select(User)).first()
    return{"db_status":result}


# -------- MODELOS --------

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    completed: bool = False
   


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks/", response_model=List[Task])
def list_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    with Session(engine) as session:
        task = session.get(Task, id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task

from fastapi import HTTPException

@app.put("/tasks/{id}", response_model=Task)
def actualizar_tarea(id: int, datos: Task, session: SessionDep):
    tarea = session.get(Task, id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tarea.title = datos.title
    tarea.description = datos.description
    tarea.completed = datos.completed
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea

@app.delete("/tasks/{id}")
def eliminar_tarea(id: int, session: SessionDep):
    tarea = session.get(Task, id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    session.delete(tarea)
    session.commit()
    return {"Ok": True}



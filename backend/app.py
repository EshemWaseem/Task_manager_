from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import Base, engine, SessionLocal
import backend.crud as crud
import backend.schemas as schemas

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://task-manager-seven-steel.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.get("/")
def root():
    return {"message": "Task Manager Backend is Running"}

@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks")
def create(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    if task.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title required")

    return crud.create_task(db, task.title)

@app.put("/tasks/{id}")
def update(id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db, id, task.title, task.completed)

@app.delete("/tasks/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    crud.delete_task(db, id)
    return {"message": "Deleted"}
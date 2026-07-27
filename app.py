from fastapi import FastAPI,Depends,HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import Base,engine,SessionLocal
import crud,schemas

Base.metadata.create_all(bind=engine)

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
)

@app.get("/tasks")
def read_tasks(db:Session=Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks")
def create(task:schemas.TaskCreate,
           db:Session=Depends(get_db)):

    if task.title.strip()=="":
        raise HTTPException(400,"Title required")

    return crud.create_task(db,task.title)

@app.put("/tasks/{id}")
def update(id:int,
           task:schemas.TaskUpdate,
           db:Session=Depends(get_db)):
    return crud.update_task(db,id,
                            task.title,
                            task.completed)

@app.delete("/tasks/{id}")
def delete(id:int,
           db:Session=Depends(get_db)):
    crud.delete_task(db,id)
    return {"message":"Deleted"}
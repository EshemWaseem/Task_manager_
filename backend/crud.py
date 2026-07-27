from sqlalchemy.orm import Session
from backend.models import Task

def get_tasks(db:Session):
    return db.query(Task).all()

def create_task(db,title):
    task=Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db,id,title,completed):
    task=db.query(Task).filter(Task.id==id).first()
    if task:
        task.title=title
        task.completed=completed
        db.commit()
        db.refresh(task)
    return task

def delete_task(db,id):
    task=db.query(Task).filter(Task.id==id).first()
    if task:
        db.delete(task)
        db.commit()
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title:str

class TaskUpdate(BaseModel):
    title:str
    completed:bool

class TaskResponse(BaseModel):
    id:int
    title:str
    completed:bool

    class Config:
        from_attributes=True
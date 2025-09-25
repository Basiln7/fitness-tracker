from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    password: str

class TaskLogCreate(BaseModel):
    task: str
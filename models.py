from pydantic import BaseModel
from typing import List ,Optional

class ShowList(BaseModel):
    id:int
    title: str
    description: str
    is_completed: bool
    class Config:
        from_attributes = True

class ListItem(BaseModel):
    id:int
    title: str
    description: str
    is_completed: bool


class UserCreate(BaseModel):
    id: int
    username: str
    email: str
    password: str
    class Config:
        from_attributes = True

class ShowUser(BaseModel):
    id: int
    name: str
    email: str 
    list_items: List[ShowList]
    class Config:
        from_attributes = True

class ShowItemWithUser(BaseModel):
    user: Optional[ShowUser] = None

    class Config:
        from_attributes = True



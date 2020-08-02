from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


# -------------------------------------------------------------------------------------------


class QuestionsCreate(BaseModel):
    id: int

    test_id: int
    question: str
    option1: str
    option2: str
    option3: str
    option4: str
    answer: int

class Attendee(BaseModel):
    id:int

    attendee_name:str
    entry_pass:str


class Answers(BaseModel):
    id:int

    marksheet_id:int
    questionTitle:str
    answer:str
    result:bool

class MarkSheet(BaseModel):
    id:int

    attendee_id:int
    test_id:int
    total_marks:int
    answers:List[Answers]=[]







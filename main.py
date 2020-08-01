from typing import Optional
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
app = FastAPI()
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
@app.get("/")
def subject_question():
    return [
        {
            "question":
            "While working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
            "option1": "answer1",
            "option2": "answer2",
            "option3": "answer3",
            "option4": "answer4",
            "correctAnswer":"option2"
        },
        {
            "question":
            "working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
            "option1": "answer1",
            "option2": "answer2",
            "option3": "answer3",
            "option4": "answer4",
            "correctAnswer":"option2"
        }]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

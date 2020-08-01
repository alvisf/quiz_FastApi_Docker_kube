from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from data_model import crud, models, schemas
from data_model.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:

        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db


# -------------------------------------------------------------------------------------------


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# ----------------------------------------------------------------------------------
@app.get("/")
def subject_question():
    return [
        {
            "question": "While working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
            "option1": "answer1",
            "option2": "answer2",
            "option3": "answer3",
            "option4": "answer4",
            "correctAnswer": "option2",
        },
        {
            "question": "working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
            "option1": "answer1",
            "option2": "answer2",
            "option3": "answer3",
            "option4": "answer4",
            "correctAnswer": "option2",
        },
    ]


@app.post("/questions/")
def create_question(question: schemas.QuestionsCreate, db: Session = Depends(get_db)):
    # db_question = crud.create_question(
    #     db,
    #     subject_name=question.subject,
    #     question=question.question,
    #     option_one=question.option1,
    #     option_two=question.option2,
    #     option_three=question.option3,
    #     option_four=question.option4,
    #     answer=question.answer,
    # )

    return crud.create_question(db=db, questions=question)

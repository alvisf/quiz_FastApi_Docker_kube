from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from data_model import crud, models, schemas
from data_model.database import SessionLocal, engine

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


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
# @app.get("/")
# def subject_question():
#     return [
#         {
#             "question": "While working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
#             "option1": "answer1",
#             "option2": "answer2",
#             "option3": "answer3",
#             "option4": "answer4",
#             "correctAnswer": "option2",
#         },
#         {
#             "question": "working with a web app, you might need to use various form controls such as text boxes, checkboxes, dropdowns, file uploads, or radio buttons in order to use HTML elements or third-party libraries for React, such as material-ui.",
#             "option1": "answer1",
#             "option2": "answer2",
#             "option3": "answer3",
#             "option4": "answer4",
#             "correctAnswer": "option2",
#         },
#     ]


@app.post("/questions/")
def create_question(question: schemas.QuestionsCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, questions=question)


@app.get("/testGen/{test_id}")
def mcq_test(test_id:str,db: Session = Depends(get_db)):
    db_questions = crud.get_questions(db=db, test_id=test_id)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="Question not found")

    return db_questions

@app.post("/createAttendee/")
def create_attendee(attendee: schemas.Attendee, db: Session = Depends(get_db)):
    db_attendee = crud.create_attendee(db=db, attendees=attendee)
    if db_attendee:
        raise HTTPException(status_code=400, detail="Error")
    return db_attendee


    
@app.post("/evaluate/", status_code=200)
def create_report(marksheet: schemas.MarkSheet, db: Session = Depends(get_db)):
    crud.create_marksheet(db=db,marksheet=marksheet)
    for answer in marksheet.answers:
        crud.create_answer(db=db,answer=answer)
    return {"description":"Success"}



# Allmarksheet

@app.get("/attendee/marksheet/{attendee_id}/{test_id}/")
def marksheet(test_id:int,attendee_id:int,db: Session = Depends(get_db)):
    db_marksheet = crud.get_marksheet(db=db, test_id=test_id,attendee_id=attendee_id)
    if db_marksheet is None:
        raise HTTPException(status_code=404, detail="Mark Sheet not found")

    return db_marksheet


@app.get("/attendee/answersheet/{attendee_id}/{test_id}/")
def answersheet(test_id:int,attendee_id:int,db: Session = Depends(get_db)):
    marksheet_id = crud.get_marksheet_id(db=db, test_id=test_id,attendee_id=attendee_id)
    db_answersheet = crud.get_answersheet(db=db,marksheet_id=marksheet_id)
    
    if db_answersheet is None:
        raise HTTPException(status_code=404, detail="Answer Sheet not found")

    return db_answersheet
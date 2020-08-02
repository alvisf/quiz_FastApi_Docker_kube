from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

    # -------------------------------------------------------------------------------------------


def create_question(db: Session, questions: schemas.QuestionsCreate):
    db_question = models.Question(
        test_id=questions.test_id,
        question=questions.question,
        option1=questions.option1,
        option2=questions.option2,
        option3=questions.option3,
        option4=questions.option4,
        answer=questions.answer,
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, test_id: int):
    return db.query(models.Question).filter(models.Question.test_id == test_id).all()

def create_attendee(db: Session, attendees: schemas.Attendee):
    db_attendee = models.Attendee(attendee_name=attendees.attendee_name, entry_pass=attendees.entry_pass)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee



def create_marksheet(db: Session, marksheet: schemas.MarkSheet):
    db_marksheet = models.MarkSheet(attendee_id=marksheet.attendee_id, test_id=marksheet.test_id,total_marks=marksheet.total_marks)
    db.add(db_marksheet)
    db.commit()
    db.refresh(db_marksheet)
    return db_marksheet

def create_answer(db: Session, answer: schemas.Answers):
    db_answer = models.Answers(questionTitle=answer.questionTitle, answer=answer.answer,result=answer.result,marksheet_id=answer.marksheet_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def get_marksheet(db: Session, test_id: int, attendee_id: int):
    return db.query(models.MarkSheet).filter(models.MarkSheet.test_id == test_id).filter(models.MarkSheet.attendee_id == attendee_id).first()

def get_marksheet_id(db: Session, test_id: int, attendee_id: int):
    return db.query(models.MarkSheet).filter(models.MarkSheet.test_id == test_id).filter(models.MarkSheet.attendee_id == attendee_id).first().id

def get_answersheet(db: Session,marksheet_id: int):
    return db.query(models.Answers).filter(models.Answers.marksheet_id == marksheet_id).all()

def get_all_marksheet(db: Session, test_id: int):
    return db.query(models.MarkSheet).filter(models.MarkSheet.test_id == test_id).all()
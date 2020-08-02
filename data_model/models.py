from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    # -------------------------------------------------------------------------------------------


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer)
    question = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    answer = Column(Integer)


class Attendee(Base):
    __tablename__ = "attendee"

    id = Column(Integer, primary_key=True, index=True)
    attendee_name = Column(String)
    entry_pass = Column(String)

    marksheet = relationship("MarkSheet", backref="test_code")


class MarkSheet(Base):
    __tablename__ = "marksheet"

    id = Column(Integer, primary_key=True, index=True)
    test_id=Column(Integer)
    total_marks=Column(Integer)
    attendee_id=Column(Integer,ForeignKey("attendee.id"))  

    answers = relationship("Answers", backref="answer_code")


class Answers(Base):
    __tablename__="answers"

    id = Column(Integer, primary_key=True, index=True)

    questionTitle=Column(String)
    answer=Column(String)
    result=Column(Boolean)
    marksheet_id=Column(Integer,ForeignKey("marksheet.id"))

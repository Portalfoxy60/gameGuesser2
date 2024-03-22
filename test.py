from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from model import Category, Word
engine = create_engine("sqlite:///wordsBase.sqlite", echo=True)

session = Session(engine)

stmt = select(Word)

for user in session.scalars(stmt):
    print(user)
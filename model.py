from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

class Base(DeclarativeBase):
     pass

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    words: Mapped[List["Word"]] = relationship(back_populates="category", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"


class Word(Base):
    __tablename__ = "words"
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(String(30))
    categoryId: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="words", cascade="all")
    def __repr__(self) -> str:
        return f"Word(id={self.id!r}, word={self.word!r}), categotyId={self.categoryId!r}, category={self.category!r}"

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    scores: Mapped[int] = mapped_column()
    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, name={self.name!r}, scores={self.scores!r})"

from typing import Dict, List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import Date
from .schema import TodoCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, index=True)
    due_date = Column(Date, index=True)


def get_todo(db: Session, todo_id: int) -> Todo:
    return db.query(Todo).filter(Todo.id == todo_id).first()


def get_todos(db: Session) -> List[Todo]:
    return db.query(Todo).order_by(Todo.due_date).all()


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    db_todo = Todo(
        title=todo.title,
        status=todo.status,
        due_date=todo.due_date
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def update_todo(db: Session, todo_id: int, todo: Dict) -> Todo:
    db.query(Todo).filter(Todo.id == todo_id).update(todo)
    db.commit()
    return db.query(Todo).filter(Todo.id == todo_id).first()


def delete_todo(db: Session, todo_id: int) -> None:
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()

    return

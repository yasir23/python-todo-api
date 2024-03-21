from typing import List
from sqlalchemy.orm.session import Session
from fastapi import Depends, FastAPI
from .db import (
    engine,
    Base,
    SessionLocal,
    get_todo,
    get_todos,
    create_todo,
    update_todo,
    delete_todo,
)
from .schema import TodoCreate, TodoUpdate


Base.metadata.create_all(bind=engine)

app = FastAPI(

)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])


@app.get("/todos")
async def readTodos(db: Session = Depends(get_db)) -> List[TodoCreate]:
    return get_todos(db)


@app.get("/todos/{id}")
async def readTodo(id: int, db: Session = Depends(get_db)) -> TodoCreate:
    return get_todo(db, todo_id=id)


@app.put("/todos/{id}")
async def updateTodo(
    id: int, todo: TodoUpdate, db: Session = Depends(get_db)
) -> TodoCreate:
    return update_todo(
        db,
        todo_id=id,
        todo={k: v for k, v in todo if v is not None}
    )


@app.post("/todos")
def createTodo(todo: TodoCreate, db: Session = Depends(get_db)) -> TodoCreate:
    return create_todo(db=db, todo=todo)


@app.delete("/todos/{id}")
async def deleteTodo(id: int, db: Session = Depends(get_db)) -> str:
    delete_todo(db=db, todo_id=id)

    return f"Todo with id {id} has been deleted"

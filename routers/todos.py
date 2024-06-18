import sys

sys.path.append("...")

from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy import asc
import models
from routers.auth import get_current_user
from database import engine, SessionLocal

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={401: {"todos": "Not Found!"}}
)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def get_all_todos_by_usr(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    todos_list = db.query(models.Todos) \
        .filter(models.Todos.owner_id == user.get("user_id")) \
        .order_by(asc(models.Todos.id)) \
        .all()
    return templates.TemplateResponse("home.html",
                                      {"request": request, "todos_list": todos_list, "user": user})


@router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()
    if not todo.complete:
        todo.complete = True
    else:
        todo.complete = False
    db.add(todo)
    db.commit()
    return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)


@router.get("/add-todo", response_class=HTMLResponse)
async def create_todo_page(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user.get("user_id")

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_page(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, title: str = Form(...), description: str = Form(...)
                    , priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    todo_model = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .first()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    db.add(todo_model)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/delete-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    todo = db.query(models.Todos) \
        .filter(models.Todos.id == todo_id) \
        .filter(models.Todos.owner_id == user.get("user_id")) \
        .first()
    if todo is None:
        return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)

    db.delete(todo)
    db.commit()
    return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)


def http_exception():
    return HTTPException(status_code=404, detail="Todo Not Found!")


def successful_response(status_code: int):
    return {"status": status_code, "transaction": "Successful"}

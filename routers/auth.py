
from datetime import timedelta, datetime
from typing import Optional


import jwt
import models

from starlette.responses import RedirectResponse
from database import engine, SessionLocal
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

SECRET_KEY = "TJVA95OrM7E2cBab30RMHrHDcEfxjoYZ"
ALG = "HS256"

models.Base.metadata.create_all(bind=engine)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    phone_number: str
    password: str


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not Authorized"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


class RegisterForm:

    def __init__(self, request: Request):
        self.request = request
        self.email: Optional[str] = None
        self.username: Optional[str] = None
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.password: Optional[str] = None
        self.v_password: Optional[str] = None

    async def create_register_form(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.username = form.get("username")
        self.first_name = form.get("first_name")
        self.last_name = form.get("last_name")
        self.password = form.get("password")
        self.v_password = form.get("v_password")


def get_password_hash(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hash_password):
    return bcrypt_context.verify(plain_password, hash_password)


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALG)


def auth_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Users) \
        .filter(models.Users.username == username) \
        .first()

    if not user:
        return False
    elif not verify_password(password, user.hashed_password):
        return False
    else:
        return user


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALG)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            return logout(request)
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=404,detail="Not Found!")


async def login_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                      db: Session = Depends(get_db)):
    user: models.Users = auth_user(form_data.username, form_data.password, db)

    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username,
                                user.id,
                                token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def auth_page(request: Request):
    user = await get_current_user(request)
    if user is not None:
        return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_token(response, form_data=form, db=db)
        if not validate_user_cookie:
            msg = "Incorrect Username/Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "UNKNOWN ERROR"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    user = await get_current_user(request)
    if user is not None:
        return RedirectResponse("/todos", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, db: Session = Depends(get_db)):
    form = RegisterForm(request)
    await form.create_register_form()
    valid_username = db.query(models.Users).filter(models.Users.username == form.username).first()
    valid_email = db.query(models.Users).filter(models.Users.email == form.email).first()
    if form.password != form.v_password or valid_username is not None or valid_email is not None:
        msg = "Invalid registration request!"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})

    user_model: models.Users = models.Users()
    user_model.email = form.email
    user_model.username = form.username
    user_model.first_name = form.first_name
    user_model.last_name = form.last_name
    user_model.hashed_password = get_password_hash(form.password)
    user_model.is_active = True
    db.add(user_model)
    db.commit()
    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})



from fastapi import FastAPI
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

# Here we change 'from app.database...' to 'from database...'
from database import engine, Base

from routers import auth, todos

def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)

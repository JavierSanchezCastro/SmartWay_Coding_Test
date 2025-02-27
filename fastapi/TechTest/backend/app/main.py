from core.Settings import settings
from db.models.Base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from db.models.Book import Book
from db.models.User import User
from db.models.Loan import Loan
from fastapi.middleware.cors import CORSMiddleware
from api.base import api_router
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from asyncio import sleep
import time
from fastapi import Request

def create_tables():
    print ("Creating tables...", flush=True)
    Base.metadata.create_all(bind=engine)

def include_router(app: FastAPI):
    app.include_router(api_router)



@asynccontextmanager
async def lifespan(app: FastAPI):
    count = 0
    while True:
        count += 1
        try:
            engine = create_engine(settings.DB_URL.unicode_string())
            connection = engine.connect()
            result = connection.execute(text("SELECT VERSION()"))
            version = result.scalar()
            print(f"Connection successful. MySQL Server Version: {version}", flush=True)
            connection.close()
            create_tables()
            break
        except OperationalError as e:
            print(f"Failed to connect to the MySQL server #{count}: {e}", flush=True)
            await sleep(1)
    #scheduler.start()
    yield
    #scheduler.shutdown()

def start_application():
    print("--------------------SMARTWAY SERVER--------------------")
    #from datetime import datetime, timezone
    app = FastAPI(title=f"{settings.PROJECT_NAME}",
                  version=settings.PROJECT_VERSION,
                  lifespan=lifespan)
    
    
    

    include_router(app)

    from fastapi import __version__ as fastapi_version
    from pydantic import __version__ as pydantic_version
    from sqlalchemy import __version__ as sqlalchemy_version
    print(f"FastAPI version: {fastapi_version}", flush=True)
    print(f"pydantic version: {pydantic_version}", flush=True)
    print(f"sqlAlchemy version: {sqlalchemy_version}", flush=True)

    return app

app = start_application()



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


from fastapi.exceptions import RequestValidationError
from fastapi import status
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extraer mensajes de error de la validación
    error_messages = [f"{error['msg']}" for error in exc.errors()]
    message = " | ".join(error_messages)  # Concatenar los mensajes si hay varios

    return templates.TemplateResponse(
        "error.html",
        {"request": request, "message": message},
        status_code=status.HTTP_400_BAD_REQUEST
    )
# FaspAPI imports
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

# 3rd party imports
import os
import time
import json

# local imports
from src.routes.file_converter import main as file_converter_main
from src.routes.youtube import main as youtube_main
from src.routes.main import main as main_router

from src.config import config
from src.routes.file_converter.schemas import FileTypeException
from src.utils.remove_old_uploads import remove_expired_files
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    version=config.VERSION, 
    title=config.APP_NAME, 
    description=config.DESCRIPTION
    )

app.include_router(main_router.router)
app.include_router(file_converter_main.router)
app.include_router(youtube_main.router)

app.mount('/public', StaticFiles(directory=config.PUBLIC_DIR),'public')
app.mount('/upload', StaticFiles(directory=config.UPLOAD_DIR),'upload')
app.mount('/static', StaticFiles(directory=config.STATIC_DIR),'static')
app.mount('/converted', StaticFiles(directory=config.CONVERTED_DIR),'converted')

templates = Jinja2Templates(directory="src/templates")


# Basic session middleware setup
app.add_middleware(SessionMiddleware,
                   secret_key="your-static-secret-key",  # Static key in production
                   max_age=3600,
                   session_cookie="my_session",
                   same_site="Lax")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Replace with your frontend domain
    allow_credentials=True,                   # Allow cookies to be sent with requests
    allow_methods=["*"],                      # Allow all methods (POST, GET, etc.)
    allow_headers=["*"]                       # Allow all headers
)



@app.exception_handler(FileTypeException)
async def unicorn_exception_handler(request: Request, exc: FileTypeException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": exc.message,
            "file_name": exc.file_name,
            "file_type": exc.file_type,
            "allowed_types": exc.allowed_types,
        },
    )


@app.on_event("startup")
@repeat_every(seconds=60*60)  # elk uur checken of er bestanden verwijderd moeten worden
def remove_expired_files_task() -> None:
    remove_expired_files(path=config.CONVERTED_DIR, expire_time=config.CONVERTED_EXPIRE_TIME)
    remove_expired_files(path=config.UPLOAD_DIR, expire_time=config.UPLOAD_EXPIRE_TIME)


@app.get("/", include_in_schema=False)
async def docs(response: Response):
    """
        Redirect naar de documentatie (`/docs/`).
    """
    response.status_code = status.HTTP_308_PERMANENT_REDIRECT
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
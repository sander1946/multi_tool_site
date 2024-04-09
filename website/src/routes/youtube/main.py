# fastapi imports
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# 3rd party imports
import shutil
import os
import hashlib
from typing import Annotated
import time

# local imports
from src.config import config
from src.routes.file_converter.schemas import FileTypeException

router = APIRouter(
    prefix="/youtube",
    tags=["youtube_downloader"],
)

templates = Jinja2Templates(directory="src/templates/youtube")

@router.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        name="main.html", context={"request": request}
    )

@router.get('/download/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.UPLOAD_DIR, file_name)
    return FileResponse(path=file_path, filename=file_name)
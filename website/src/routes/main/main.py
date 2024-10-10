# fastapi imports
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import zipfile
from io import BytesIO
from fastapi.responses import StreamingResponse

# 3rd party imports
import shutil
import os
import hashlib
from typing import Annotated
import time
from src.utils.image_coverter import Converter
from typing import List

# local imports
from src.config import config
from src.routes.file_converter.schemas import FileTypeException

router = APIRouter(
    prefix="",
    tags=["landing_page"],
)

templates = Jinja2Templates(directory=os.path.join(config.BASE_DIR, "src/templates/main"))

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        name="main.html", context={"request": request,
        }
    )

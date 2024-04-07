# fastapi imports
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# 3rd party imports
import shutil
import os
import hashlib
from typing import Annotated

# local imports
from src.config import config
from src.routes.file_converter.schemas import FileTypeException

router = APIRouter(
    prefix="/convert",
    tags=["file_converter"],
)

templates = Jinja2Templates(directory="src/templates/file_converter")

@router.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse(
        name="main.html", context={"request": request}
    )


@router.post('/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    allowed_types = ["application/json", "image/jpeg", "image/png", "image/svg+xml", "video/mp4"]
        
    if file.content_type not in allowed_types:
        raise FileTypeException(file.filename, file.content_type, allowed_types)
    
    hash = hashlib.md5(str(file.filename).encode("utf-8"))
    new_filename = f"{hash.hexdigest()}.{config.EXTENTIONS[file.content_type]}"

    save_path = os.path.join(config.UPLOAD_DIR, new_filename)
    with open(save_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)
        print(f"File {file.filename} saved as {new_filename} in {config.UPLOAD_DIR}")
    return templates.TemplateResponse(
        name="main.html", 
        context={
            "request": request,
            'FileResponse': FileResponse(path=save_path, media_type=file.content_type, filename=new_filename),
            'file_name': file.filename,
            'content': file.content_type,
            'path': save_path,
            'image_url': f"/upload/{new_filename}"
        }
    )


@router.get('/download/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.UPLOAD_DIR, file_name)
    return FileResponse(path=file_path, filename=file_name)
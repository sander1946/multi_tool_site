# fastapi imports
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# 3rd party imports
import shutil
import os
import hashlib
from typing import Annotated
import time
from src.utils.image_coverter import Converter

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
    allowed_types: list[str] = ["image/jpeg", "image/png", "image/svg+xml", "video/mp4"]
    string_types = ""
    for type in allowed_types:
        string_types += f"{type}, "
    
    return templates.TemplateResponse(
        name="main.html", context={"request": request,
            "allowed_types": string_types
        }
    )


@router.post('/')
async def upload(request: Request, image: UploadFile = File(...)):    
    allowed_types: list[str] = ["image/jpeg", "image/png", "image/svg+xml", "video/mp4"]
    string_types = ""
    for type in allowed_types:
        string_types += f"{type}, "
    print(string_types)
        
    if image.content_type not in allowed_types:
        raise FileTypeException(image.filename, image.content_type, allowed_types)
    
    hash = hashlib.md5(str(image.filename).encode("utf-8"))
    new_filename = f"{hash.hexdigest()}.{config.EXTENTIONS[image.content_type]}"
    new_filename = new_filename[-10:]
    save_path = os.path.join(config.UPLOAD_DIR, new_filename)
    with open(save_path, "wb+") as f:
        shutil.copyfileobj(image.file, f)
        print(f"File {image.filename} saved as {new_filename} in {config.UPLOAD_DIR}")
    return templates.TemplateResponse(
        name="main.html", 
        context={
            "request": request,
            'FileResponse': FileResponse(path=save_path, media_type=image.content_type, filename=new_filename),
            'file_name': new_filename,
            'content': image.content_type,
            'path': save_path,
            'image_url': f"/upload/{new_filename}",
            "allowed_types": string_types
        }
    )
    
@router.post('/convert/{file_name}')
async def convert(request: Request, file_name: str, image_type: str):
    converter = Converter(file_name)
    new_filename = converter.convert(image_type)
    return templates.TemplateResponse(
        name="main.html", 
        context={
            "request": request,
            'FileResponse': FileResponse(path=os.path.join(config.UPLOAD_DIR, new_filename), media_type=image_type, filename=new_filename),
            'file_name': new_filename,
            'content': image_type,
            'path': os.path.join(config.UPLOAD_DIR, new_filename),
            'image_url': f"/upload/{new_filename}"
        }
    )


@router.get('/download/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.UPLOAD_DIR, file_name)
    return FileResponse(path=file_path, filename=file_name)
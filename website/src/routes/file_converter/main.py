# fastapi imports
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import zipfile
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Form


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
    prefix="/convert",
    tags=["file_converter"],
)

templates = Jinja2Templates(directory=os.path.join(config.BASE_DIR, "src/templates/file_converter"))

@router.get("/")
async def read_item(request: Request):
    allowed_types: list[str] = ["image/jpeg", "image/png", "image/svg+xml", "video/mp4", "image/webp"]
    string_types = ""
    for type in allowed_types:
        string_types += f"{type}, "
    
    return templates.TemplateResponse(
        name="main.html", context={"request": request,
            "allowed_types": string_types
        }
    )


@router.post('/')
async def upload(request: Request, images: List[UploadFile] = File(...), convert_to: str = Form(...)):    
    allowed_types: list[str] = ["image/avif", "image/gif", "image/png", "image/jpeg", "image/jpg", "image/webp", "image/svg+xml", "image/x-icon"]
    string_types = ", ".join(allowed_types)
    # Retrieve or initialize the list of saved files for this session
    saved_files = []

    for image in images:
        if image.content_type not in allowed_types:
            raise FileTypeException(image.filename, image.content_type, allowed_types)    

        hash = hashlib.md5(str(image.filename).encode("utf-8"))
        filename = f"{hash.hexdigest()}.{config.EXTENTIONS[image.content_type]}"
        filename = filename[-15:]
        save_path = os.path.join(config.CONVERTED_DIR, filename)
        
        with open(save_path, "wb+") as f:
            shutil.copyfileobj(image.file, f)
            # print(f"File {image.filename} saved as {new_filename} in {config.CONVERTED_DIR}")
        
        # Convert the file to PNG
        converter = Converter(filename)
        try:
            new_filename, e = converter.convert(convert_to)
        except Exception as error:
            return {"error": "Failed to convert the image",
                    "desciption": str(error)}
        if e:
            return {"error": "Failed to convert the image",
                    "desciption": str(e).split("`")[0]}
        
        print(f"File {filename} converted to {new_filename}")
        
        if convert_to not in ["avif", "gif", "png", "jpeg", "jpg", "webp", "svg", "ico"] and image.content_type in ["image/avif", "image/gif", "image/png", "image/jpeg", "image/jpg", "image/webp", "image/svg+xml", "image/x-icon"]:
            print(f"Invalid file type: {convert_to}")
            new_filename = filename
        
        # Append the file to the list of files for this session
        saved_files.append({
            'original_filename': image.filename,
            'saved_filename': filename,
            'png_filename': new_filename,
            'content_type': image.content_type,
            'path': save_path,
            'image_url': f"/converted/{new_filename}",
            'image_extension': convert_to.upper()
        })
    
    # Save the list of converted files to the session
    request.session['converted_files'] = saved_files

    return templates.TemplateResponse(
        name="main.html", 
        context={
            "request": request,
            "files": saved_files,
            "allowed_types": string_types
        }
    )


@router.get('/download/{file_name}')
async def download(file_name: str):
    file_path = os.path.join(config.CONVERTED_DIR, file_name)
    return FileResponse(path=file_path, filename=file_name)


@router.post('/zip_download')
async def download_all_images_as_zip(request: Request):
    # Retrieve the list of files from the session
    files_to_zip = request.session.get('converted_files', [])

    if not files_to_zip:
        return {"error": "No files to download."}

    # Create an in-memory zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for file in files_to_zip:
            file_path = os.path.join(config.CONVERTED_DIR, file['png_filename'])
            zip_file.write(file_path, arcname=file['png_filename'])  # Add file to the zip

    zip_buffer.seek(0)

    # Return the zip file as a download response
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={
        f"Content-Disposition": "attachment; filename=converted_images.zip"
    })

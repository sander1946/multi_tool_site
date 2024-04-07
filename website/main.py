# FaspAPI imports
from fastapi import FastAPI, Response, status, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 3rd party imports

# local imports
from src.routes.file_converter import main as file_converter_main
from src.config import config
from src.routes.file_converter.schemas import FileTypeException


app = FastAPI(
    version=config.VERSION, 
    title=config.APP_NAME, 
    description=config.DESCRIPTION
    )


app.include_router(file_converter_main.router)

app.mount('/public', StaticFiles(directory='public'),'public')
app.mount('/upload', StaticFiles(directory='upload'),'upload')

templates = Jinja2Templates(directory="src/templates")

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
import os

VERSION: str = '0.1.1'
APP_NAME: str = 'API'
DESCRIPTION: str = 'API voor de website'
BASE_DIR: str = os.getcwd()
UPLOAD_DIR: str = os.path.join(BASE_DIR, "upload")
STATIC_DIR: str = os.path.join(BASE_DIR, "public")

EXTENTIONS: dict[str, str] = {
    "application/json": "json",
    "application/x-yaml": "yaml",
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/svg+xml": "svg",
    "text/plain": "txt",
    "text/csv": "csv",
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/vnd.ms-excel": "xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-powerpoint": "ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "video/mp4": "mp4",
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "application/zip": "zip",
    "application/x-tar": "tar",
    "application/gzip": "gz",
    "application/x-bzip2": "bz2",
    "application/x-7z-compressed": "7z",
    "application/x-rar-compressed": "rar",
    "video/x-msvideo": "avi",
    "video/x-ms-wmv": "wmv",
    "video/webm": "webm",
    "audio/ogg": "ogg",
    "audio/flac": "flac",
    "video/mpeg": "mpg",
    "video/mpeg": "mpeg",
    "image/webp": "webp",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/tiff": "tiff",
    "image/tiff": "tif",
    "image/heic": "heic",
    "image/heif": "heif",
    "image/heic-sequence": "heics",
    "image/heif-sequence": "heifs",
    "image/avif": "avif",
    "image/apng": "apng",
    "image/x-icon": "ico",
    "image/x-icon": "cur",
    "application/pdf": "pdf",
    "application/xml": "xml"
}
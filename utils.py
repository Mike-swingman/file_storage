import os
import hashlib
from enum import StrEnum, auto
from flask import current_app


class AllowedExtensions(StrEnum):
    TXT = auto()
    PDF = auto()
    PNG = auto()
    JPG = auto()
    JPEG = auto()
    GIF = auto()


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1] in iter(AllowedExtensions)


def get_hash_file(file) -> str:
    file.seek(0)
    hasher = hashlib.sha256()
    # Чтение файла чанками по 64 кб
    while chunk := file.read(65536):
        hasher.update(chunk)
    file.seek(0)
    return hasher.hexdigest()


def get_path_file(hash_filename: str, to_dir: bool = False) -> str:
    path_file = os.path.join(current_app.config["UPLOAD_FOLDER"], hash_filename[:2])
    if to_dir:
        return path_file
    else:
        return os.path.join(path_file, hash_filename)

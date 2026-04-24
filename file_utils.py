"""File utility helpers."""
import os


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, 'w') as f:
        f.write(content)


def file_exists(path: str) -> bool:
    return os.path.isfile(path)


def get_extension(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.lstrip('.')


def list_files(directory: str, extension: str = None) -> list[str]:
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            if extension is None or entry.endswith(f'.{extension}'):
                files.append(full_path)
    return sorted(files)

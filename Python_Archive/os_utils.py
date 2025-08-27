import os
from typing import Optional

def get_script_dir() -> str:
    """
    Returns the absolute path to the folder where the current script is located.
    """
    return os.path.dirname(os.path.abspath(__file__))

def get_project_root(script_dir: Optional[str] = None) -> str:
    """
    Returns the project root (one level up from the script directory).
    If script_dir is not provided, it defaults to the caller's location.
    """
    if script_dir is None:
        script_dir = get_script_dir()
    return os.path.abspath(os.path.join(script_dir, ".."))

def join_path(*args: str) -> str:
    """
    Joins multiple strings into a safe OS path.
    """
    return os.path.join(*args)

def file_exists(path: str) -> bool:
    """
    Checks if a file or folder exists at the given path.
    """
    return os.path.exists(path)

def ensure_dir(path: str) -> None:
    """
    Creates a directory (and any necessary parent directories) if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)

def get_full_path_from_script(relative_path: str) -> str:
    """
    Joins a relative path to the script directory to get the full absolute path.
    """
    return join_path(get_script_dir(), relative_path)

def get_full_path_from_root(relative_path: str) -> str:
    """
    Joins a relative path to the project root directory to get the full absolute path.
    """
    return join_path(get_project_root(), relative_path)

def list_files_in_dir(path: str) -> list:
    """
    Returns a list of file names in the given directory.
    """
    if not file_exists(path):
        return []
    return [f for f in os.listdir(path) if os.path.isfile(join_path(path, f))]

def list_dirs_in_dir(path: str) -> list:
    """
    Returns a list of folder names in the given directory.
    """
    if not file_exists(path):
        return []
    return [d for d in os.listdir(path) if os.path.isdir(join_path(path, d))]

def get_data_file(*path_parts):
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(ROOT_DIR, "data", *path_parts)

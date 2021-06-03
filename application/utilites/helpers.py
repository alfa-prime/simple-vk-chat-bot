from pathlib import Path
import shutil

def make_dir(dir_name):
    """ проверяет наличие директории и в случае отсуствия создаёт ёё """
    dir_name = Path.cwd() / dir_name
    if not dir_name.exists():
        Path.mkdir(dir_name)

def remove_dir(dir_name):
    shutil.rmtree(dir_name, ignore_errors=True)

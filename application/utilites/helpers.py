import pathlib

def make_dir(dir_name):
    """ проверяет наличие директории и в случае отсуствия создаёт ёё """
    dir_name = pathlib.Path.cwd() / dir_name
    if not dir_name.exists():
        pathlib.Path.mkdir(dir_name)

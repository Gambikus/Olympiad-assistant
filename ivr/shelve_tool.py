import shelve


def set_shelve(filename, key, value):
    with shelve.open(filename) as file:
        file[key] = value


def get_shelve(filename, key):
    with shelve.open(filename) as file:
        return file[key]


def exist_shelve(filename, key):
    with shelve.open(filename) as file:
        return key in file


def del_shelve(filename, key):
    with shelve.open(filename) as file:
        del file[key]

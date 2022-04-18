from __future__ import annotations

from aiogram.types import InputFile


photos = {}


def get_photo(a: str):
    if a in photos:
        return photos[a]
    else:
        xa = a + '.jpg' if '.' not in a else a[:-4] + a[-4:]
        set_photo(a, InputFile(f'assets/img/{xa}'))
        return photos[a]


def set_photo(a: str, b: str | InputFile):
    global photos
    photos[a] = b
    return b

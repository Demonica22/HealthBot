from .english import localization as eng_loc
from .russian import localization as rus_loc

DEFAULT_LANG = "en"
AVAILABLE_LANGS = {
    "en": "English",
    "ru": "Русский"
}


def get_text(param: str, lang: str = "ru"):
    if lang == "ru":
        return rus_loc[param]
    elif lang == "en":
        return eng_loc[param]

    return eng_loc[param]

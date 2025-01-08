from enum import Enum


class DiseasesResponseFormat(str, Enum):
    json = "json"
    docx = "docx"
    html = "html"


class UserLanguage(str, Enum):
    en = "en"
    ru = "ru"

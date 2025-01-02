from src.handlers.user import user_router
from src.handlers.main_menu import main_router
from src.handlers.back import back_router
from src.handlers.disease import disease_router
from aiogram import Router

routers: list[Router] = [
    back_router,
    main_router,
    disease_router,

    user_router, # Должен быть последним т.к. есть обработка всех сообщения
]

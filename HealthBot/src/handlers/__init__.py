from src.handlers.user import user_router
from src.handlers.main_menu import main_router
from src.handlers.back import back_router
from aiogram import Router

routers: list[Router] = [user_router,
                         back_router,
                         main_router,
                         ]

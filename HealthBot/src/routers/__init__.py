from src.routers.user import user_router
from src.routers.main_menu import main_router
from src.routers.back import back_router
from src.routers.disease import disease_router
from src.routers.notifications import notification_router
from src.routers.doctor import doctor_router
from aiogram import Router

routers: list[Router] = [
    back_router,
    main_router,
    disease_router,
    notification_router,
    doctor_router,
    user_router,  # Должен быть последним т.к. есть обработка всех сообщения
]

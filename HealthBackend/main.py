from fastapi import FastAPI
from src.utils.lifespan import lifespan
from src.users.router import router as user_router
from src.diseases.router import router as disease_router
from src.notifications.router import router as notifications_router
from src.doctors.router import router as doctor_router
app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(doctor_router)
app.include_router(disease_router)
app.include_router(notifications_router)

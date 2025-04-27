from fastapi import FastAPI
from app.controllers import log_controller

app = FastAPI(title="AI Health & Wellness Tracker")

app.include_router(log_controller.router)

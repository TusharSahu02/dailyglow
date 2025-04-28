from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.user_input import UserInput
from app.database.connection import db
from app.services.openai_service import parse_user_input
from app.utils.logger import logger
from app.models.daily_log import DailyLog
from datetime import datetime

router = APIRouter()


@router.post("/log")
async def log_user_input(user_input: UserInput):
    structured_data = await parse_user_input(user_input.message)
    # valid_log = DailyLog(**structured_data)

    # log_to_save = valid_log.dict()
    structured_data["date"] = datetime.utcnow().date().isoformat()

    result = await db.daily_logs.insert_one(structured_data)

    logger.info(f"Data saved for user {result.inserted_id}")

    # Convert ObjectId to string and update structured_data
    structured_data["_id"] = str(result.inserted_id)

    # Return only one response
    return JSONResponse(
        status_code=200, content={"status": "success", "data": structured_data}
    )

from openai import RateLimitError, APIError
import asyncio
from functools import wraps
from typing import Tuple


# Generic Retry Decorator with Exponential Backoff
def retry_on_exception(
    max_retries: int = 3,
    initial_delay_seconds: int = 2,
    backoff_factor: int = 2,
    exceptions: Tuple[Exception] = (Exception,),
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay_seconds
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    await asyncio.sleep(delay)
                    delay *= backoff_factor  # Exponential backoff

        return wrapper

    return decorator


# Specific Retry Decorators (Ready to Import)

retry_on_rate_limit = retry_on_exception(
    max_retries=5,
    initial_delay_seconds=2,
    backoff_factor=2,
    exceptions=(RateLimitError,),  # Updated exception
)

retry_on_api_error = retry_on_exception(
    max_retries=3,
    initial_delay_seconds=5,
    backoff_factor=2,
    exceptions=(APIError,),  # Updated exception
)

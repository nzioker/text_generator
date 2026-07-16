from fastapi import Request, status, HTTPException
import redis
import time

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def rate_limiter(request: Request):
    user_id = request.client.host

    current_window = int(time.time() // 60)

    redis_key = f"rate:{user_id}:{current_window}"
    
    current_requests = redis_client.incr(redis_key)

    if current_requests == 1:
        redis_client.expire(redis_key, 60)

    if current_requests > 10:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceededd. Max 10 requests per minute.")
    return True
    



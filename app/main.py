"""###############################################
## Statistics service for the websites.
## Save page views and other statistics for the websites.
## Use Redis to store the data.
## Collect the data from the Redis database and send it to the main service using celery.

Structure:

"domain_hash": {
    "path_hash": {
        "views": 0,
    }
}
#################################################"""

import aioredis
import os
import json

from fastapi import FastAPI, Request

from app.helpers import hash_string, get_domain, get_path

app = FastAPI()

# Connect to the redis database
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

redis_db = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


@app.on_event("startup")
async def startup_event():
    # Initialize Redis connection
    # (aioredis handles this in the from_url method, so this might be optional)
    ...


@app.on_event("shutdown")
async def shutdown_event():
    # Close Redis connection
    await redis_db.close()


@app.post("/website/save/")
async def save_website(request: Request):
    # Get url from request
    params = await request.json()
    url = params.get("url")

    # Hash the url
    domain_hash = hash_string(get_domain(url))

    # Retrieve from Redis
    domain_result = await redis_db.get(domain_hash)

    if domain_result:
        # Deserialize the result
        domain_result = json.loads(domain_result)
    else:
        domain_result = {}

    # Path
    path = get_path(url)

    # Retrieve from Redis
    path_result = domain_result.get(path)

    if path_result:
        # Add one to the views
        domain_result[path]["views"] += 1
    else:
        # Create path
        domain_result[path] = {"views": 1}

    # Serialize the result
    serialized_result = json.dumps(domain_result)

    await redis_db.set(domain_hash, serialized_result)
    return {"status": 200}


@app.put("/website/")
async def get_websites(request: Request):
    # Get url from request
    params = await request.json()
    url = params.get("url")

    # Retrieve from Redis
    domain_hash = hash_string(get_domain(url))

    domain_result = await redis_db.get(domain_hash)

    if domain_result:
        # Deserialize the result
        domain_result = json.loads(domain_result)
        return {"status": 200, "data": domain_result}

    return {"status": 404}


@app.get("/")
async def read_main(request: Request):
    return {"status": 200}

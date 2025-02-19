from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from redis.asyncio import Redis
from configs.config import logger

import os
from dotenv import find_dotenv, load_dotenv

from configs import redis, config
from model_training import ModelTraining

# Redis Connection
r = Redis(host="redis", port=6379, decode_responses=True)


# Load environment variables
load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    yield

    # Shutdown logic
    if redis.redis:
        await redis.redis.close()


app = FastAPI(
    lifespan=lifespan,
    title=config.PROJECT_NAME,
)
# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["File-Path", "Content-Disposition"],
)


class TrainRequest(BaseModel):
    epochs: int
    user_id: str


def train_model(epochs: int, user_id: str):
    """Run model training as a background task."""
    model_training = ModelTraining(user_id)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "data.yml")
    training_result_path = "./results"
    os.makedirs(training_result_path, exist_ok=True)
    model_training.train_yolov8_model(config_path, epochs, training_result_path)


@app.post("/train", tags=["training"])
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    """API endpoint to start training."""
    background_tasks.add_task(train_model, request.epochs, request.user_id)
    return {"message": "Training started"}


@app.get("/progress/{user_id}", tags=["training"])
async def get_progress(user_id: str) -> EventSourceResponse:
    async def event_generator():
        pubsub = r.pubsub()
        await pubsub.subscribe(f"training_progress_{user_id}")
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":

                    data = message["data"]
                    logger.info("Data: ", data)
                    logger.info("#" * 50)
                    yield {"event": "message", "data": f"{data}\n\n"}
        finally:
            await pubsub.unsubscribe(f"training_progress_{user_id}")

    return EventSourceResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Access-Control-Allow-Credentials": "true",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
            "Access-Control-Allow-Origin": "*",
        },
    )


@app.get("/")
async def root():
    return {"message": "Welcome to training API"}

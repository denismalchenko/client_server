import asyncio
import redis.asyncio as aioredis
import httpx
import uvicorn
import os
import logging
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from uuid import uuid4, UUID
from typing import List
from dotenv import load_dotenv
from urllib.parse import urlparse
from colorlog import ColoredFormatter

from task import Task, Status

tasks = []
load_dotenv()
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
endpoint = os.getenv('ENDPOINT')
timeout = int(os.getenv('TIMEOUT'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:%(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

redis_connection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_connection
    redis_connection = aioredis.Redis(auto_close_connection_pool=False)
    if timeout > 0:
        asyncio.create_task(cleanup_cache(redis_connection))
    yield
    redis_connection.close()


app = FastAPI(
    title="Crawler",
    description="Crawl urls",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get('/')
async def root():
    return {"message": "Server is running"}


@app.post(endpoint, response_model=Task, status_code=201)
async def read_urls(urls: List[str]) -> Task:
    tasks.append(Task(id=uuid4(), status=Status.running, result=urls))
    asyncio.create_task(do_task(tasks[-1], len(tasks) - 1))
    return tasks[-1]


@app.get(f'{endpoint}{{task_id}}', response_model=Task, status_code=200)
async def read_task(task_id: UUID):
    found_task = find_task(task_id)
    if found_task and found_task.status == Status.ready:
        return found_task
    else:
        raise HTTPException(status_code=404,
                            detail="Task not found or not ready")


async def cleanup_cache(redis_connection) -> None:
    while True:
        await asyncio.sleep(timeout)
        await redis_connection.flushdb()
        logger.info('\tCache cleaned!')


def find_task(task_id):
    return next((task for task in tasks if task.id == task_id), None)


async def find_in_redis(redis_connection, url):
    cached_data = await redis_connection.hget('hash', url)
    return cached_data


async def do_task(task: Task, task_index: int) -> None:
    urls = set(add_http_prefix(task.result))
    global redis_connection
    response = []
    count_from_cache = count_from_connection = 0
    async with httpx.AsyncClient() as client:
        for url in urls:
            found_in_redis = await find_in_redis(redis_connection, url)
            if found_in_redis is not None:
                count_from_cache += 1
                response.append({url: int(found_in_redis)})
            else:
                count_from_connection += 1
                resp = await client.get(url)
                response.append({url: resp.status_code})
                await redis_connection.hset('hash', url, resp.status_code)
            await redis_connection.hincrby('urls', url)
            await redis_connection.hincrby('domains', urlparse(url).netloc)
    tasks[task_index].status = Status.ready
    tasks[task_index].result = response
    logger.info(
        f'\tTask {task.id} results: {count_from_connection} from connection, {count_from_cache} from cache.'
    )
    logger.info('\turls counters:')
    print_from_redis(await redis_connection.hgetall('urls'))
    logger.info('\tdomains counters:')
    print_from_redis(await redis_connection.hgetall('domains'))


def print_from_redis(redis_dict: dict) -> None:
    for key, value in redis_dict.items():
        print(f"{key.decode('utf-8')}: {int(value)}")


def add_http_prefix(urls: List[str]) -> List[str]:
    for i, url in enumerate(urls):
        if not url.startswith('http://') and not url.startswith('https://'):
            urls[i] = 'http://' + url
    return urls


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)

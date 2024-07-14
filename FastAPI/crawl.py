import httpx
import asyncio
import argparse
import os
import logging
from dotenv import load_dotenv
from colorlog import ColoredFormatter

from task import Task

load_dotenv()
host = os.getenv('HOST')
port = int(os.getenv('PORT'))
endpoint = os.getenv('ENDPOINT')
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


def parce_args() -> int:
    parser = argparse.ArgumentParser(description='queryable URL')
    parser.add_argument('urls',
                        type=str,
                        nargs='+',
                        help='One or more url arguments')
    return parser.parse_args().urls


async def crawl(urls: list) -> Task:
    async with httpx.AsyncClient(base_url=f'http://{host}:{port}') as client:
        response = await client.post(endpoint, json=urls)
        if response.status_code == 201:
            task = Task(**response.json())
            logger.info(
                f'\tTask created: {task.id} {task.status} {task.result}')
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
        return task


async def result(task: Task) -> None:
    status_codes = 0
    while status_codes != 200:
        async with httpx.AsyncClient(
                base_url=f'http://{host}:{port}') as client:
            response = await client.get(f'{endpoint}{task.id}')
            status_codes = response.status_code
            if response.status_code == 200:
                task_result = Task(**response.json())
                print('----- Task results: -----')
                for key, value in [(v, k) for url in task_result.result
                                   for k, v in url.items()]:
                    print(f'{value}\t{key}')


if __name__ == '__main__':
    urls = parce_args()
    try:
        task = asyncio.run(crawl(urls))
        asyncio.run(result(task))
    except Exception as exc:
        logger.error(exc)

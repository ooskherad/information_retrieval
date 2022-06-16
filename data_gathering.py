import asyncio
import json

import httpx as httpx
import requests
from bs4 import BeautifulSoup


class DataGathering:
    _semaphore = asyncio.BoundedSemaphore(4)
    _try_number = 5

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    @classmethod
    async def get_data(cls, url: str):
        for i in range(cls._try_number):
            try:
                async with cls._semaphore:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, timeout=None)
                        resp.raise_for_status()
                        return resp.text
            except Exception as exception:
                await asyncio.sleep(i * 5)
                print(exception)

    @classmethod
    async def crawl_data(cls, url: str):
        return BeautifulSoup(await cls.get_data(url), 'html.parser')

    @classmethod
    async def select_crawl_data(cls, url: str, selector: str):
        soup = await cls.crawl_data(url)
        return soup.select(selector)

    def run(self, function, **kwargs):
        self.loop.run_until_complete(function(**kwargs))

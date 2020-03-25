"""Fetch latest COVID-19 cases in Sweden."""
from aiohttp import ClientSession, ClientResponseError
from dataclasses import dataclass
from datetime import datetime

import logging


@dataclass
class SweRegion:
    """Class for holding country stats."""

    URL = "https://www.svt.se/special/articledata/2322/folkhalsomyndigheten.json"
    NAME = "SVT Datajournalistik"

    id: str
    region: str
    confirmed: int
    deaths: int
    updated: datetime

    @staticmethod
    def from_json(item):
        return SweRegion(
            id=item["kod"],
            region=item["region"],
            confirmed=item["fall"],
            deaths=item["avlidna"],
            updated=datetime.fromtimestamp(item["ts"] / 1000),
        )


async def get_cases(session: ClientSession, *, source=SweRegion):
    """Fetch Corona Virus cases in Sweden."""
    resp = await session.get(source.URL)
    data = await resp.json(content_type=None)

    results = []

    for item in data:
        try:
            if item['days'] is 0:
                results.append(source.from_json(item))
        except KeyError:
            logging.getLogger(__name__).warning("Got wrong data: %s", item)

    return results

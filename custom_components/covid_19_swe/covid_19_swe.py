"""Fetch latest COVID-19 cases in Sweden."""
from aiohttp import ClientSession, ClientResponseError
from dataclasses import dataclass
import logging


@dataclass
class SweRegion:
    """Class for holding country stats."""

    URL = "https://www.svt.se/special/articledata/2322/sverige.json"
    NAME = "SVT"

    id: str
    region: str
    confirmed: int
    deaths: int
    updated: int

    @staticmethod
    def from_json(item, last_updated):
        return SweRegion(
            id=item["kod"],
            region=item["namn"],
            confirmed=item["antal"],
            deaths=item["dead"],
            updated=last_updated,
        )


async def get_cases(session: ClientSession, *, source=SweRegion):
    """Fetch Corona Virus cases in Sweden."""
    resp = await session.get(source.URL)
    data = await resp.json(content_type=None)

    results = []

    for item in data["data"]:
        try:
            results.append(source.from_json(item, data["data_updated"]))
        except KeyError:
            logging.getLogger(__name__).warning("Got wrong data: %s", item)

    return results

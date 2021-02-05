"""Fetch latest COVID-19 cases in Sweden."""
from aiohttp import ClientSession, ClientResponseError
from dataclasses import dataclass
from datetime import datetime

import logging


@dataclass
class SweRegion:
    """Class for holding country stats."""

    URL = "https://services5.arcgis.com/fsYDFeRKu1hELJJs/arcgis/rest/services/FOHM_Covid_19_FME_1/FeatureServer/0/query?f=geojson&where=Region%20%3C%3E%20%27dummy%27&returnGeometry=false&outFields=*"
    NAME = "Folkhälsomyndigheten"

    id: str
    region: str
    confirmed: int
    deaths: int
    updated: datetime

    @staticmethod
    def from_json(item):
        return SweRegion(
            id=item["OBJECTID"],
            region=item["Region"],
            confirmed=item["Totalt_antal_fall"],
            deaths=item["Totalt_antal_avlidna"],
            updated=datetime.now(),
        )


async def get_cases(session: ClientSession, *, source=SweRegion):
    """Fetch Corona Virus cases in Sweden."""
    resp = await session.get(source.URL)
    data = await resp.json(content_type=None)

    results = []
    for item in data['features']:
        try:
            results.append(source.from_json(item['properties']))
        except KeyError:
            logging.getLogger(__name__).warning("Got wrong data: %s", item)

    return results

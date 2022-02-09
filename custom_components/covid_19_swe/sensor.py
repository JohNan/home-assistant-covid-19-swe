"""Sensor platform for the COVID-19 Sweden cases."""
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity

from . import get_coordinator
from .const import ATTRIBUTION, OPTION_ALL_REGIONS

SENSORS = {
    "confirmed": "mdi:emoticon-neutral-outline",
    "deaths": "mdi:emoticon-dead-outline",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    coordinator = await get_coordinator(hass)

    async_add_entities(
        Covid19SweSensor(coordinator, config_entry.data["region"], info_type)
        for info_type in SENSORS
    )


class Covid19SweSensor(Entity):
    """Sensor representing corona virus data."""

    name = None
    unique_id = None

    def __init__(self, coordinator, region, info_type):
        """Initialize coronavirus sensor."""
        if region == OPTION_ALL_REGIONS:
            self.name = f"All regions COVID-19 Sweden {info_type}"
        else:
            self.name = f"{coordinator.data[region].region} COVID-19 Sweden {info_type}"
        self.unique_id = f"{region}-{info_type}"
        self.coordinator = coordinator
        self.region = region
        self.info_type = info_type

    @property
    def available(self):
        """Return if sensor is available."""
        return self.coordinator.last_update_success and (
            self.region in self.coordinator.data or self.region == OPTION_ALL_REGIONS
        )

    @property
    def state(self):
        """State of the sensor."""
        if self.region == OPTION_ALL_REGIONS:
            return sum(
                getattr(case, self.info_type) for case in self.coordinator.data.values()
            )

        return getattr(self.coordinator.data[self.region], self.info_type)

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.info_type]

    @property
    def unit_of_measurement(self):
        """Return unit of measurement."""
        return "people"

    @property
    def extra_state_attributes(self):
        """Return device attributes."""
        return {ATTR_ATTRIBUTION: ATTRIBUTION}

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.coordinator.async_add_listener(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """When entity will be removed from hass."""
        self.coordinator.async_remove_listener(self.async_write_ha_state)

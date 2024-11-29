"""All constants used globally across the integration."""

from logging import Logger, getLogger

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

NAME = "Starling Home Hub Integration"
DOMAIN = "starling_home_hub"
VERSION = "1.0.4"
ATTRIBUTION = "Based on the Starling Home Hub Developer Connect API"

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.SWITCH,
    # Platform.CAMERA,
]

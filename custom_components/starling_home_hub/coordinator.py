"""Handles data updates coordinators."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.starling_home_hub.api import (StarlingHomeHubApiClient, StarlingHomeHubApiClientAuthenticationError,
                                                     StarlingHomeHubApiClientError)
from custom_components.starling_home_hub.const import DOMAIN, LOGGER
from custom_components.starling_home_hub.models.api.device import Device, DeviceUpdate
from custom_components.starling_home_hub.models.api.stream import StartStream, StreamStatus
from custom_components.starling_home_hub.models.coordinator import CoordinatorData


class StarlingHomeHubDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    data: CoordinatorData

    def __init__(
        self,
        hass: HomeAssistant,
        client: StarlingHomeHubApiClient,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=5),
        )
        self.client = client

    async def start_stream(self, device_id: str, sdp_offer: str) -> StartStream:
        """Start a stream."""
        return await self.client.async_start_stream(device_id=device_id, sdp_offer=sdp_offer)

    async def stop_stream(self, device_id: str, stream_id: str) -> StreamStatus:
        """Stop a stream."""
        return await self.client.async_stop_stream(device_id=device_id, stream_id=stream_id)

    async def extend_stream(self, device_id: str, stream_id: str) -> StreamStatus:
        """Extend a stream."""
        return await self.client.async_extend_stream(device_id=device_id, stream_id=stream_id)

    async def update_device(self, device_id: str, update: dict) -> DeviceUpdate:
        """Update a device."""
        return await self.client.async_update_device(device_id=device_id, update=update)

    async def fetch_data(self) -> CoordinatorData:
        """Fetch data for the devices."""

        devices = await self.client.async_get_devices()
        status = await self.client.async_get_status()

        full_devices: dict[str, Device] = {}
        for device in devices:
            full_device = await self.client.async_get_device(device_id=device["id"])
            full_devices[device["id"]] = full_device

        self.data = CoordinatorData(devices=full_devices, status=status)

        return self.data

    async def refresh_data(self) -> bool:
        """Refresh data."""
        data = await self.fetch_data()
        self.async_set_updated_data(data)

        return True

    async def _async_update_data(self) -> CoordinatorData:
        """Update data via library."""

        try:
            return await self.fetch_data()
        except StarlingHomeHubApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except StarlingHomeHubApiClientError as exception:
            raise UpdateFailed(exception) from exception

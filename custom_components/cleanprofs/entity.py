from __future__ import annotations  # Enable postponed evaluation of type hints (Py<3.11 compatibility)

import json
from pathlib import Path

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def _read_manifest_version() -> str | None:
    """Read the integration version from manifest.json.

    Returns:
        The version string from manifest.json (key: "version"), or None if:
        - the file cannot be read,
        - the JSON is invalid,
        - the key is missing.
    """
    try:
        # manifest.json is located in the same folder as this file (custom_components/cleanprofs/)
        manifest_path = Path(__file__).parent / "manifest.json"

        # Load and parse the manifest so we can use its version as the device software version
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        return manifest.get("version")
    except Exception:
        # Never break entity setup because of a version-read problem
        return None

_MANIFEST_VERSION = _read_manifest_version()


class CleanProfsBaseEntity(CoordinatorEntity):
    """Base Entity for all CleanProfs entities."""

    # Let HA treat the entity name as a sub-name under the device name
    # (often results in nicer naming in the UI)
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry) -> None:
        """Initialize the base entity with a coordinator and config entry."""
        super().__init__(coordinator)
        self._entry = entry  # Keep reference to the config entry for stable device identifiers

    @property
    def device_info(self) -> DeviceInfo:
        """Return Home Assistant DeviceInfo for grouping entities under one device.

        Home Assistant will group all entities that return the same identifiers
        into a single Device.
        """
        return DeviceInfo(
            # Unique and stable per config entry: gives 1 device per configured account/instance
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="CleanProfs",
            manufacturer="Hessels Automation",
            model="Cleaning schedule API",
            sw_version=_MANIFEST_VERSION,
        )
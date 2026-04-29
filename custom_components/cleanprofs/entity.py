from __future__ import annotations

import json
from pathlib import Path

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


def _read_manifest_version() -> str | None:
    try:
        manifest_path = Path(__file__).parent / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        return manifest.get("version")
    except Exception:
        return None


_MANIFEST_VERSION = _read_manifest_version()


class CleanProfsBaseEntity(CoordinatorEntity):
    """Base Entity for all CleanProfs entities"""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry) -> None:
        super().__init__(coordinator)
        self._entry = entry

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="CleanProfs",
            manufacturer="Hessels Automation",
            model="Cleaning schedule API",
            sw_version=_MANIFEST_VERSION,
        )
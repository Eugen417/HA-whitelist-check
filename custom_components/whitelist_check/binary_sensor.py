from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for host in coordinator.data.keys():
        entities.append(WhitelistSensor(coordinator, host, entry.entry_id))

    async_add_entities(entities)

class WhitelistSensor(CoordinatorEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(self, coordinator, host: str, entry_id: str):
        super().__init__(coordinator)
        self.host = host
        self.entry_id = entry_id
        self._attr_unique_id = f"{entry_id}_{host.replace('://', '_').replace('/', '_')}"

        # НА ТИВНАЯ ДЕАКТИВАЦИЯ: Указываем Home Assistant, включать ли датчик по умолчанию
        host_data = self.coordinator.data.get(self.host, {})
        config = host_data.get("config", {}) if host_data else {}
        self._attr_entity_registry_enabled_default = config.get("enabled_default", True)

    @property
    def name(self) -> str:
        host_data = self.coordinator.data.get(self.host, {})
        config = host_data.get("config", {}) if host_data else {}
        return config.get("name", self.host)

    @property
    def is_on(self) -> bool:
        host_data = self.coordinator.data.get(self.host, {})
        return host_data.get("is_online", False) if host_data else False

    @property
    def extra_state_attributes(self):
        host_data = self.coordinator.data.get(self.host, {})
        config = host_data.get("config", {}) if host_data else {}
        return {
            "target_host": self.host,
            "method": config.get("method", "GET/Auto"),
            "description": config.get("description", "Нет описания")
        }

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.entry_id)},
            name="Мониторинг белого списка",
            manufacturer="Custom Integration",
            model="Network Checker",
            entry_type="service", 
        )

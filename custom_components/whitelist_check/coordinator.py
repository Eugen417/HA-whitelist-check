import asyncio
import logging
import async_timeout
from datetime import timedelta
from urllib.parse import urlparse

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# Обновляем импорты констант
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, DEFAULT_HOSTS, CONF_CUSTOM_HOSTS, CONF_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class WhitelistUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        # Достаем интервал в секундах из настроек (или берем дефолтные 300)
        interval_seconds = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval_seconds),
        )
        self.entry = entry
        self.session = async_get_clientsession(hass)

    def get_all_hosts(self):
        hosts = DEFAULT_HOSTS.copy()
        custom = self.entry.options.get(CONF_CUSTOM_HOSTS, {})
        if isinstance(custom, dict):
            hosts.update(custom)
        return hosts

    async def _async_update_data(self):
        hosts = self.get_all_hosts()
        results = {}

        tasks = [self._check_host(host, hosts[host]) for host in hosts.keys()]
        statuses = await asyncio.gather(*tasks)

        for host, status in zip(hosts.keys(), statuses):
            results[host] = {
                "config": hosts[host],
                "is_online": status
            }
        
        return results

    async def _check_host(self, host: str, config: dict) -> bool:
        method = config.get("method", "GET")

        # Если выбран строгий PING
        if method == "PING":
            clean_host = host
            if "://" in host:
                try:
                    parsed = urlparse(host)
                    clean_host = parsed.hostname or host
                except Exception:
                    pass
            return await self._check_ping(clean_host)

        # Веб-запросы
        if host.startswith("http://") or host.startswith("https://"):
            return await self._check_http(host, method)
        else:
            return await self._check_tcp(host)

    async def _check_http(self, url: str, method: str) -> bool:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        try:
            async with async_timeout.timeout(5):
                async with self.session.request(method, url, allow_redirects=True, headers=headers) as response:
                    if response.status < 500:
                        return True
        except Exception:
            pass
        
        # Фолбек: если веб-запрос упал, пробуем системный пинг
        try:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            if host:
                return await self._check_ping(host)
        except Exception:
            pass
        return False

    async def _check_tcp(self, host: str) -> bool:
        if host in ["1.1.1.1", "8.8.8.8", "77.88.8.1", "77.88.8.8"]:
            port = 53
        elif host.endswith(".com") or host.endswith(".org") or host.endswith(".ru"):
            port = 443
        else:
            port = 80
            
        try:
            future = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(future, timeout=3)
            writer.close()
            await writer.wait_closed()
            return True
        except Exception:
            pass
        
        # Фолбек: если порт закрыт, пробуем системный пинг
        return await self._check_ping(host)

    async def _check_ping(self, host: str) -> bool:
        try:
            process = await asyncio.create_subprocess_exec(
                "ping", "-c", "1", "-W", "2", host,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.communicate()
            return process.returncode == 0
        except Exception:
            return False

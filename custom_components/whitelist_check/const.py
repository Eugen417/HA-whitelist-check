from datetime import timedelta

DOMAIN = "whitelist_check"
CONF_CUSTOM_HOSTS = "custom_hosts"

UPDATE_INTERVAL = timedelta(minutes=5)

# Базовый список критичных сервисов
DEFAULT_HOSTS = {
    # Базовые инфраструктурные сервисы HA
    "https://github.com": {
        "name": "GitHub",
        "description": "Критично для работы HACS"
    },
    "https://api.github.com": {
        "name": "GitHub API",
        "description": "Проверка обновлений интеграций"
    },
    
    # IoT и умный дом
    "https://developer.home-connect.com": {
        "name": "Home Connect API",
        "description": "Облако Bosch/Siemens"
    },
    "https://on.dcl.csa-iot.org": {
        "name": "CSA IoT DCL",
        "description": "Distributed Compliance Ledger (Matter/Zigbee)",
        "enabled_default": False  # Будет отключен по умолчанию в UI
    },
    "https://device-heartbeat-chn-17b3df92.linklinkiot.com": {
        "name": "LinkLink IoT",
        "description": "Облачные сервисы LinkLink",
        "enabled_default": False  # Будет отключен по умолчанию в UI
    },
    "https://openapi.tuyaeu.com": {
        "name": "Tuya Cloud (EU)",
        "description": "Облачные API Tuya (Европа)",
        "enabled_default": False  # Будет отключен по умолчанию в UI
    },
    "https://ota.matter.ikea.com": {
        "name": "IKEA Matter OTA",
        "description": "Сервер обновлений прошивок IKEA",
        "enabled_default": False  # Будет отключен по умолчанию в UI
    },

    # Глобальный интернет
    "1.1.1.1": {
        "name": "Cloudflare DNS",
        "description": "Глобальный интернет (Cloudflare)"
    },
    "8.8.8.8": {
        "name": "Google DNS",
        "description": "Глобальный интернет (Google)"
    },

    # Рунет / Локальная связность
    "77.88.8.1": {
        "name": "Yandex DNS (Primary)",
        "description": "Проверка доступности Рунета"
    },
    "77.88.8.8": {
        "name": "Yandex DNS (Secondary)",
        "description": "Проверка доступности Рунета"
    },
    "https://ya.ru": {
        "name": "Ya.ru",
        "description": "Проверка веб-доступа к Рунету"
    }
}

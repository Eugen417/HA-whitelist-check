# 🌐 White List Check for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/Eugen417/HA-whitelist-check?style=for-the-badge)](https://github.com/Eugen417/HA-whitelist-check/releases)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-compatible-blue.svg?style=for-the-badge&logo=home-assistant)](https://www.home-assistant.io/)
[![GitHub Stars](https://img.shields.io/github/stars/Eugen417/HA-whitelist-check.svg?style=for-the-badge)](https://github.com/Eugen417/HA-whitelist-check/stargazers)
[![License](https://img.shields.io/github/license/Eugen417/HA-whitelist-check.svg?style=for-the-badge)](https://github.com/Eugen417/HA-whitelist-check/blob/main/LICENSE)
[![HA Validation](https://img.shields.io/github/actions/workflow/status/Eugen417/HA-whitelist-check/validate.yml?style=for-the-badge&label=HA%20Validation)](https://github.com/Eugen417/HA-whitelist-check/actions)

Мощный и легкий компонент для Home Assistant, предназначенный для мониторинга доступности сетевых узлов, API-сервисов, IoT-облаков и транзитных шлюзов.

Идеально подходит для сложных сетей с VPN-маршрутизацией, проверкой "белых списков" (White Lists) и отслеживанием статуса рунета.

## ✨ Возможности

* **100% Управление через UI (Config Flow):** Никакой правки YAML. Добавляйте, изменяйте и удаляйте хосты прямо из интерфейса Home Assistant в пару кликов.
* **Гибкий интервал опроса:** Настраивайте частоту проверок (от 10 секунд до 24 часов) прямо в интерфейсе без перезагрузки системы. Нужна моментальная реакция на падение VPN-туннеля? Просто укажите нужный интервал.
* **Умные проверки (Smart Fallback):** Интеграция умеет проверять узлы по HTTP (GET, POST, HEAD, PUT). Если IoT-сервер сбрасывает HTTP-запрос (как это делает Tuya или LinkLink) или отвечает нестандартной ошибкой API, движок автоматически всё анализирует или переключается на системный `PING` (ICMP).
* **Свой метод для каждого хоста:** Возможность жестко задать метод `PING` для устройств без веб-интерфейса (например, телевизоров или локальных Zigbee-шлюзов).
* **Нативная интеграция с HA:** Все проверяемые узлы аккуратно сгруппированы под одним виртуальным устройством. Вы можете включать и отключать мониторинг конкретных узлов стандартными средствами HA.
* **Обход блокировок ботов:** Имитация реального браузера (User-Agent) при HTTP-проверках, чтобы такие сервисы, как Яндекс или Cloudflare, не блокировали мониторинг.

## 🛠 Установка

### Через HACS (В один клик)

[![Открыть в Home Assistant и установить White List Check через HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Eugen417&repository=HA-whitelist-check&category=integration)

> **Примечание:** Если кнопка не работает, добавьте репозиторий в HACS вручную по инструкции ниже.

### Вручную (Через пользовательские репозитории)

1. Откройте **HACS** > **Integrations**.
2. Нажмите три точки в правом верхнем углу > **Custom repositories**.
3. Вставьте ссылку на репозиторий: `https://github.com/Eugen417/HA-whitelist-check`
4. Выберите категорию **Integration** и нажмите **Add**.
5. Установите появившуюся интеграцию **White List Check**.
6. Перезагрузите Home Assistant.

## 🚀 Использование и настройка

1. Перейдите в **Настройки** -> **Устройства и службы**.
2. Нажмите **Добавить интеграцию** и найдите `White List Check`.
3. После добавления у вас появится новое устройство с базовым набором сенсоров (GitHub, Cloudflare, Yandex и др.).
4. **Управление своими хостами:** Нажмите на кнопку **Настроить** (шестеренку) на карточке интеграции. Откроется меню, где вы сможете:
   * Добавить свой IP, локальный шлюз или сайт.
   * Изменить название или метод проверки существующего хоста.
   * Удалить неактуальный узел.
   * **Задать глобальный интервал опроса** (в секундах) для всех датчиков.

> **Примечание:** Узкоспециализированные IoT-хосты (CSA IoT, LinkLink, Tuya, IKEA OTA) добавлены в систему, но **отключены по умолчанию**, чтобы не нагружать сеть. Если они вам нужны, включите их через настройки сущности в Home Assistant.

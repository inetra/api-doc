title: Media Locator API
quotes language: french
version: 1.0
status: черновик

# Введение

Данный документ создан для унификации способов получения информации о местах расположения контента из медийных каталогов, таких, как каталог фильмов или расписание выпусков телепередач канала.

<span style="color:#f00">TODO</span>: находится ли в рамках данного API получение информации об источниках вещания эфиров телеканалов провайдера? Стоит ли поддерживать что-то кроме M3U и XSPF?

# Взаимодействие с API

API подразумевает доступ только аутентифицированного пользователя (возможно, анонимного), пользующегося авторизованным приложением. Таким образом здесь закладывается возможность внедрения системы оплаты для получения контента.

В следствие чего данное API должно быть доступно только по HTTPS. Формат запроса:

	https://<path_to_api>/<api_version>/<method>.<format>?token=<token>[&params]

Где:

- `path_to_api` — путь до API, полученный в Регистратуре
- `api_version` — мажорная версия API (должна быть равна `1`)
- `path_to_elem` — путь до элемента, над которым производится действие
- `method` — метод, который производится над элементом
- `token` — токен доступа, полученный на сервере аутентификации пользователя и авторизации приложения
- `format` — формат упаковки данных

Формат упаковки параметров в теле ответа (или в теле запроса) может быть одним из:

- `json` — JSON;
- `protobuf` — Google Protocol Buffers.

Значения всех параметров перед передачей серверу необходимо кодировать для предотвращения неоднозначной интерпретации так, как это рекомендуется в [RFC3986].

[RFC3986]: http://tools.ietf.org/html/rfc3986

# Методы

## locations - Получение ссылок на контент

Дополнительные параметры:

- `id` — список идентификаторов элементов каталога, чьи источники запрашиваются

Формат ответа: сообщение `CatalogueItemLocationsInfo`

	enum LocationType {
	  option allow_alias = true;
	  MAGNET = 0;
	  HTTP = 1;
	  HLS = 2;
	  UDP_MULTICAST = 3;
	  RTSP = 4;
	}
	
	message CatalogueItemLocation {
	  optional LocationType type = 1;
	  repeated string locations = 2;
	}
	
	message CatalogueItemLocationInfo {
	  optional int64 catalogue_item_id = 1;
	  repeated CatalogueItemLocation locations = 2;
	}
	
	message CatalogueItemLocationsInfo {
	  repeated CatalogueItemLocationInfo locations_info = 1;
	}

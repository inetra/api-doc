title: Media Locator API
quotes language: french
version: 1.0
status: черновик

# Введение

Данный документ создан для унификации способов получения информации о местах расположения контента из медийных каталогов, таких, как каталог фильмов или расписание выпусков телепередач канала[^fn-todo_streaming].

Логика взаимодействия клиентского ПО, серверов Регистратуры и серверов Оператора-вещателя подразумевает согласованность идентификаторов выпусков телепрограмм (далее в тексте – id). В настоящем документе не описывается механизм согласования идентификаторов.

[^fn-todo_streaming]:<span style="color:#f00">TODO Q1</span>: находится ли в рамках данного API получение информации об источниках вещания эфиров телеканалов провайдера? Стоит ли поддерживать что-то кроме M3U и XSPF?   
<span style="color:#080">TODO A1</span>: предлагаю (пока) НЕ вносить в этот документ информацию об адресах вещания телеканалов. Возможно, когда-нибудь потом.

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

Коды ответов сервера *должны* соответствовать стандартным кодам HTTP-ответов для соответствующих ситуаций. Если по запросу не найдено никакой информации, сервер *должен* вернуть нормальный (код 200) пустой ответ.


[RFC3986]: http://tools.ietf.org/html/rfc3986

# Методы

## locations - Получение ссылок на контент

| Наименование | Значение по-умолчанию | Описание |
|:------------:|:---------------------:|----------|
|`id`          | нет                   | Список логических идентификаторов элементов каталога. Необязательный, однако его отсутствие приведёт к пустому ответу сервера. |
[Дополнительные параметры][tbl-locations-params]

Замечание: Важно не путать элемент медийного каталога, например, выпуск телепередачи (Issue), и экземпляр записи или фильма (Rip). Используемые в настоящем API идентификаторы id являются элементами каталога.

Формат ответа: сообщение `CatalogueItemLocationsInfo`[^fn-repeated_locations] [^fn-metainfo-todo]

	enum UriType {
	  option allow_alias = true;
	  MAGNET = 0;
	  HTTP = 1;
	  HLS = 2;
	  UDP_MULTICAST = 3;
	  UDP = 3;
	  RTSP = 4;
	}
	
	message Location {
	  optional UriType type = 1;
	  optional string uri = 2;
	  optional float usage_probability = 3; // for load balancing
	}
	
	enum TrackType {
	  VIDEO = 0;
	  AUDIO = 1;
	  SUBTITLE = 2;
	}
	
	message TrackInfo {
	  optional int64 id = 1;
	  optional TrackType type = 2;
	  optional int32 codec_id = 3; // from MediaInfo
	  optional int32 language = 4; // ISO code
	  optional int32 duration = 5; // in seconds
	  optional int32 bitrate = 6; // in bytes per second
	  optional Location locations = 7;
	  // for video
	  optional int32 width = 8; // in pixels
	  optional int32 height = 9; // in pixels
	  // for audio
	  optional int32 channel_count = 10;
	}
	
	message MediaPart {
	  repeated TrackInfo tracks = 1;
	  repeated Location locations = 2; // load balance
	}
	
	message Rip {
	  optional int64 id = 1;
	  repeated MediaParts parts = 2; // multipart source
	  repeated string snapshots = 3; // for quality comparison
	}
	
	message CatalogueItemRipInfo {
	  optional int64 catalogue_item_id = 1;
	  repeated Rip rips = 2;
	  optional int32 error = 3;
	}
	
	message CatalogueItemLocationsReply {
	  repeated CatalogueItemRipInfo rip_info = 1;
	}

Отсутствие в ответе информации по запрошенному id следует интерпретировать как «информация для указанного id не найдена».
В текущей версии API все другие ошибки ответов по конкретным id предлагается интерпретировать как «информация для указанного id не найдена»[^fn-errors-todo].

[^fn-repeated_locations]: Требует уточнение интерпретации *множественных* адресов для одного элемента в сообщении `CatalogueItemLocation`.  
Не описано поведение клиента при наличии в ответе множественных сообщений CatalogueItemLocationInfo с совпадающим catalogue_item_id.

[^fn-metainfo-todo]: Предлагаю внести необязательную дополнительную метаинформацию для экземпляра произведения (rip), для облегчения выбора экземпляра для воспроизведения на стороне клиента. По аналогии с другими API, где указывается размер картинки, кодек и т.п..

[^fn-errors-todo]: TODO: В последующих версиях API можно определить перечень ответов для типичных ошибок сервера, таких, как нет информации, недостаточно прав, неверный формат запроса и т.п..

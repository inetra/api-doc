title: Promo API
quotes language: french
version: 1.1
status: черновик

# Введение

Данный документ описывает программный интерфейс (API) сервиса Promo.

Сервис предоставляет клиентам информацию об активации промо–кодов, контрагентам — информацию об активных акциях и возможность добавлять и изменять существующие промо–коды.

В случае отсутствия сервиса в выдаче "[Регистратуры][registry.md]" клиент должен скрыть функцию ввода промо–кода.

## Термины и определения

В этом документе используются термины и определения, описанные в документах "[О программных интерфейсах сервисов Инетры][about.md]" и "[Термины и определения][terms.md]".

[terms.md]: terms.md#media-guide-anchor
[about.md]: about.md
[registry.md]: registry.md

# Взаимодействие с API

Точка входа определяется [Регистратурой][registry.md], при этом числовой идентификатор сервиса — `14`, строковый — `promo`.

API подразумевает доступ только аутентифицированного пользователя (возможно, анонимного), пользующегося авторизованным приложением.

Запросы формируются следующим образом:

	https://<path_to_api>/<method>.<format>?[parameters]

Где:

- `path_to_api` — путь до API, полученный из Регистратуры;
- `method` — имя метода;
- `format` — формат передачи данных, может быть одним из:
	- `json` — JSON;
	- `protobuf` — Google Protocol buffers.
- `parameters` — дополнительные параметры метода.

Данные аутентификации могут быть переданы посредством параметра запроса или при помощи HTTP заголовка `Authorization` с указанием схемы авторизации `OAuth`, например:

	Authorization: OAuth 7f17a012c73abe1603d9a1

## Общие параметры

Параметр | тип    | значение
---------|--------|----------
`token`  |`строка`| токен аутентифицированного пользователя

Токен может быть получен при помощи [Auth API][auth-api-doc].

[auth-api-doc]: auth.md

# Клиентские методы Promo API

## `activation_info` — получение информации об активации промо–кода

Дополнительные параметры метода:

Параметр | тип    | значение
---------|--------|----------
`promo`  |`строка`| введенный пользователем промо–код

Формат ответа: сообщение [`ActivationInfo`][p-activation-info].

# Методы межсерверного взаимодействия Promo API (<span style="color:#0f0"> Новое в 1.1 </span>)

## `actions` — получение списка активных акций контрагента

Дополнительных параметров метода нет.

Формат ответа: сообщение [`ActionsList`][p-actions-list].

## `modify` — выполнение запросов на добавление или обновление промо–кодов.

Дополнительные параметры передаются в теле запроса методом POST. Формат запроса — сообщение `PromoModifyRequests`, кодируется форматом, указанным в параметре запроса.

К активной акции может быть добавлен один промо–код или несколько, для этого необходимо буквенно–цифровой код в атрибуте `code` и срок действия при помощи атрибутов `start_time`, `end_time`. Срок действия промо–кода не должен выходить за рамки срока действия акции.

>	TODO: доработать метод modify

В рамках активной акции можно задать или изменить срок действия промо–кода, указав атрибуты `code_id`, `start_time`, `end_time`.

Формат ответа: сообщение [`ModifyResult`][p-modify-result].

# Описания форматов способом Google Protocol Buffers

## ActivationInfo — информация об активации промо–кода [p-activation-info]

	enum PromoCodeStatus {
	  NOT_FOUND = 1;
	  EXPIRED = 2;
	  FOUND = 3;
	}

	message ActivationInfo {
	  optional PromoCodeStatus status = 1;
	  optional uint32 contractor_id = 2;
	  optional string private_office_url = 3;
	}

Замечания:

- `status` — статус активации промо–кода:
	- `NOT_FOUND` — промо–код не найден;
	- `EXPIRED` — срок действия промо–кода истек;
	- `FOUND` — промо–код найден, для данного статуса будут переданы атрибуты `contractor_id` и `private_office_url`.
- `contractor_id` — числовой идентификатор контрагента;
- `private_office_url` — адрес ["Личного кабинета"][anchor-private-office] контрагента, который должен быть использован для активации промо–кода.

[anchor-private-office]: iptv.md#anchor-personal-office

## ActionsList — список активных акций [p-actions-list]

	message ActionsList {
	  repeated PromoAction actions = 1;
	}

Замечания:

- `actions` — список активных акций.

## PromoAction — промо–акция [p-promo-action]

	message PromoAction {
	  optional uint32 action_id = 1;
	  optional string title = 2;
	  optional uint64 start_time = 3;
	  optional uint64 end_time = 4;
	  repeated PromoCode promo_codes = 5;
	}

Замечания:

- `action_id` — числовой идентификатор акции;
- `title` — название акции;
- `start_time` — дата и время начала акции в формате Unix–time;
- `end_time` — дата и время окончания акции в формате Unix–time;
- `promo_codes` — список промо–кодов акции.

## PromoCode — промо–код [p-promo-code]

	message PromoCode {
	  optional uint32 code_id = 1;
	  optional string code = 2;
	  optional uint64 start_time = 3;
	  optional uint64 end_time = 4;
	}

Замечания:

- `code_id` — числовой идентификатор промо–кода;
- `code` — буквенно–цифровой код;
- `start_time` — дата и время начала действия промо–кода;
- `end_time` — дата и время окончания действия промо–кода;

Если атрибуты `start_time` и `end_time` не указаны — значит срок действия промо–кода совпадает со сроком действия акции.

## PromoModifyRequests — список запросов на добавление или обновление промо–кодов [p-modify-requests]

	message PromoModifyRequests {
	  repeated PromoModifyRequest requests = 1;
	}

## PromoModifyRequest — запрос на добавление или обновление промо–кода [p-modify-request]

	enum RequestType {
	  ADD = 1;
	  UPDATE = 2;
	}

	message PromoModifyRequest {
	  optional RequestType type = 1;
	  optional uint32 action_id = 2;
	  repeated PromoCode codes = 3;
	}

# Изменения по версиям

## Изменения в версии 1.0 (TVREC-378)

- описан метод `activation_info` для получения информации об активации промо–кода.

## Изменения в версии 1.1 (TVREC-378)

- описаны методы межсерверного взаимодействия.
title: Promo API
quotes language: french
version: 1.0
status: черновик

# Введение

Данный документ описывает программный интерфейс (API) сервиса Promo.

Сервис предоставляет информацию об активации промо–кодов.

В случае отсутствия сервиса в выдаче "[Регистратуры][registry.md]" клиент должен скрыть функцию ввода промо–кода.

[registry.md]: registry.md

## Термины и определения

В этом документе используются термины и определения, описанные в документах "[О программных интерфейсах сервисов Инетры][about.md]" и "[Термины и определения][terms.md]".

[terms.md]: terms.md#private-office-anchor
[about.md]: about.md

# Взаимодействие с API

Точка входа определяется [Регистратурой][registry.md], числовой идентификатор сервиса — `14`, строковый — `promo`.

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

Данные аутентификации могут быть переданы по схеме `Bearer` (см. [RFC6750]) посредством параметра запроса `access_token` или при помощи HTTP заголовка `Authorization` с указанием схемы авторизации `Bearer`, например:

	Authorization: Bearer 7f17a012c73abe1603d9a1

[RFC6750]: http://tools.ietf.org/html/rfc6750

## Общие параметры

 параметр     | тип    | значение
--------------|--------|----------
`access_token`|`строка`| токен аутентифицированного пользователя

Токен может быть получен при помощи [Auth API][auth-api-doc].

[auth-api-doc]: auth.md

# Методы

## `activation_info` — получение информации об активации промо–кода

Дополнительные параметры метода:

Параметр      | тип    | значение
--------------|--------|----------
`promo`       |`строка`| введенный пользователем промо–код

Формат ответа: сообщение [`ActivationInfo`][p-activation-info].

# Описания форматов способом Google Protocol Buffers

## ActivationInfo — информация об активации промо–кода [p-activation-info]

	enum ActivationErrorСode {
	  PROMO_CODE_NOT_FOUND = 1;
	  PROMO_CODE_EXPIRED = 2;
	}

	message ActivationInfo {
	  optional ActivationErrorСode error_code = 1;

	  optional uint32 contractor_id = 2;
	  optional string private_office_uri = 3;
	}

Замечания:

- `error_code` — код ошибки активации:
	- `PROMO_CODE_NOT_FOUND` — не найден указанный промо–код;
	- `PROMO_CODE_EXPIRED` — истек срок действия промо–кода.
- `contractor_id` — числовой идентификатор контрагента;
- `private_office_uri` — адрес "Личного кабинета" контрагента, на основе которого необходимо [сформировать адрес для активации промо–кода][private-office-doc].

[private-office-doc]: private-office.md#activate-promo-code

# Изменения по версиям

## Изменения в версии 1.0 (TVREC-378)

- Начальная редакция документа;
- Описан метод `activation_info` для получения информации об активации промо–кода.

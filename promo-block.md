title: PromoBlock API
quotes language: french
version: 1.0
status: согласован

# Введение

Данный сервис предоставляет данные для отображения промоблока (слайдера/карусели). 

# Размещение и использование.

Точка входа определяется [Регистратурой][registry-api-ref], где числовой идентификатор сервиса - `22`, строковый - `promo_block`.

Запросы формируются следующим образом:

[registry-api-ref]: registry.md

	http://<path_to_api>/<api_version>/<method>.<format>?[parameters]
    
Где:

- `path_to_api` — путь до API, полученный из Регистратуры
- `api_version` — версия API 
- `method` — имя метода
- `format` — формат передачи данных, может быть одним из:
	- `json` — JSON
- `parameters` — параметры метода

Значения всех параметров необходимо кодировать для предотвращения неоднозначной интерпретации так, как это рекомендуется в [RFC3986].

[RFC3986]: http://tools.ietf.org/html/rfc3986

## Общие параметры запросов

Для формировании ответа с учетом особенностей клиента, во все запросы необходимо включать следующие общие параметры:

параметр   | формат  | по умолчанию | смысл
-----------|---------|--------------|----------------
`access_token` | `строка` | отсутствует | Токен доступа, полученный при помощи [Auth API][auth-doc]

[auth-doc]: auth.md

# Методы PromoBlock API

## `select` --- получение набора креативов для отображения в промоблоке

параметр   | формат  | по умолчанию | смысл
-----------|---------|--------------|----------------
`profileName` | `строка` | отсутствует | Желаемый профиль картинки для [CreativeImage][p-creative-image] - картинки других профилей будут откинуты из каждого креатива (но сами креативы будут возвращены, даже если из них были откинуты все картинки)

Формат ответа: сообщение [`CreativeList`][p-creative-list].

Пример запроса
 
	GET /promo_block/1/select.json?access_token=...

# Форматы сообщений

## CreativeList --- список креативов для показа в промоблоке [p-creative-list]

    message CreativeList {
        repeated Creative items = 1;
    }

## Creative --- креатив, один элемент промоблока

    message Creative {
        required uint64 id = 1;
        optional string title = 2;
        optional string subtitle = 3;
        optional uint64 endPublication = 4;
        repeated CreativeImage images = 5;
        optional CreativeContent contentItem = 6;
    }

Пояснение:

- `id` — идентификатор креатива
- `title` - заголовок для вывода пользователю поверх картинки креатива
- `subtitle` - подзаголовок для вывода пользователю поверх картинки креатива
- `endPublication` - время окончания публикации креатива в формате UNIX-seconds: в этот момент времени креатив исчезнет из выдачи API, также в этот момент времени клиент самостоятельно без доп. запросов может удалить из промоблока данный креатив
- `images` - список картинок в разных профилях, клиент может игнорировать креатив, если подходящая картинка отсутствует
- `contentItem` - контент, связанный с креативом - предполагается, что креатив ведёт на страницу этого контента

## CreativeImage --- картинка креатива в одном профиле [p-creative-image]

    message CreativeImage {
        required string url = 1;
        required string profile = 2;
        optional uint32 width = 3;
        optional uint32 height = 4;
    }

Пояснение:

- `url` - адрес картинки
- `profile` - профиль картинки, определяющий её размер и формат; возможные значение:
    - `smarttv_promo_block` - картинка для вывода в промоблоке смарт тв
    - `mobile_promo_block` - картинка для вывода в промоблоке мобилок
- `width` - широта картинки в пикселях
- `height` - высота картинки в пикселях

## CreativeContent --- контент, связанный с креативом

    message CreativeContent {
        required string type = 1;
        optional uint64 id = 2;
        optional uint64 channelId = 3;
        optional string title = 4;
        optional uint64 startTime = 5;
        optional uint64 endTime = 6;
        optional bool showLive = 7;
    }

Пояснение:

- `type` - тип контента креатива; возможные значения:
    - "channel" - канал
    - "telecast" - передача в будущем (анонс), настоящем (эфир) или прошлом (архив)
    - "movie" - фильм
    - "series" - сериал
    - "tv-show" - ТВ-шоу
- `id` - идентификатор контента
- `channelId` - доп. идентификатор канала (когда `type` = "telecast")
- `title` - название контента, которое можно использовать для вывода в UI клиента
- `startTime` - начало эфира (когда `type` = "telecast") в формате UNIX-seconds
- `endTime` - окончание эфира (когда `type` = "telecast") в формате UNIX-seconds
- `showLive` - нужно ли во время эфира (когда `type` = "telecast") заменять картинку креатива прямой трансляцией

# История версий

## Версия 1.0

Начальная версия (PTVRND-894)

- описан метод сервиса PromoBlock `select`.
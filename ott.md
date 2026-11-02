---
title: OTT API
version: 1.7
server-version: 1.7
status: не согласован
quotes language: french
---

# Общая информация

OTT API - специальный API для конфигурирования HLS-AAA (он же OTT-Auth), который позволяет оператору целиком и полностью управлять каналами и потоками вещания.

# Требования

## Общие
* Формат ответа: JSON;
* Кодировка: UTF-8;
* Рекомендуемый Content-Type: `application/json; charset=UTF-8`.

## К сериализации в JSON
* не допускается переименовывание полей, изменение стиля (например, на camelCase) и регистра;
* boolean сериализуется как true | false;
* ENUM сериализуется с преобразованием в integer;
* спецсимволы в строках должны быть экранированы согласно стандартам JSON (ECMA-404, RFC4627).

# Методы

## `channels` - получение информации о каналах и потоках

### Формат ответа

#### Сообщение ChannelList <a id="m-channellist"></a>

 параметр    | формат |     статус     | описание
-------------|--------|----------------|----------
 `title`     | строка |  обязательный  | при генерации списка каналов будет использовано в качестве названия (title)
 `channels`  | список |  обязательный  | список каналов: набор полей из сообщения [Channel][p-channel] через запятую
 `categories`| список | необязательный | список категорий: набор полей из сообщения [Category](#m-category) через запятую
 
Замечания:
* Порядок, в котором каналы перечисляются в категориях, будет использован при генерации плейлистов;
* Порядок, в котором передаются каналы, будет использован для сортировки некатегоризированных каналов при генерации плейлистов.

Подробнее: [Protocol Buffers][p-channellist]
 
#### Сообщение Channel <a id="m-channel"></a>

 параметр         | формат |     статус     | описание
------------------|--------|----------------|----------
 `id`             | число  |  обязательный  | Единый постоянный идентификатор канала, совпадающий с использующимся RADIUS-сервером
 `alias`          | строка |  обязательный  | Единый постоянный текстовый идентификатор канала
 `title`          | строка |  обязательный  | Человекочитаемое название канала
 `streams`        | список |  обязательный  | Источники вещания канала, см. [StreamSource][m-streamsource]
 `identifier_url` | строка | необязательный | Ссылка на страницу канала на сайте
 `schedule_url`   | строка | необязательный | Ссылка на программу телепередач
 `logo_url`       | строка | необязательный | Ссылка на логотип канала
 `status`         | число  | необязательный | Статус канала: тестовое (0) / боевое вещание (1)

Подробнее: [Protocol Buffers][p-channel]

#### Сообщение StreamSource <a id="m-streamsource"></a>

 параметр         | формат |     статус     | описание
------------------|--------|----------------|----------
 `id`             | число  |  обязательный  | Постоянный идентификатор (например, порядковый номер) потока в рамках канала
 `url`            | строка |  обязательный  | URL источника. Если тип источника HLS_VARIANT (2), можно передать пустую строку, и тогда URL будет автоматически сгенерирован согласно конфигурации HLS-AAA
 `protected_path` | строка | необязательный | Требуется для источника типа HLS (0), для всех остальных можно не указывать.
 `type`           | число  |  обязательный  | Тип источника: HLS (0), UDP (1), HLS_VARIANT (2), RAW (3). RAW используется для отдачи адреса источника в виде "как есть".
 `substreams`     | список | необязательный | Список потоков типа HLS (0), требуется указывать только для источника типа HLS_VARIANT (2). Не допускается степень вложенности больше 1.
 `bandwidth`      | строка | необязательный | Согласно стандарту HLS
 `resolution`     | строка | необязательный | Согласно стандарту HLS
 `codecs`         | строка | необязательный | Согласно стандарту HLS
 `audio`          | строка | необязательный | Согласно стандарту HLS
 `name`           | строка | необязательный | Хак для некоторых плееров - указание степени качества картинки. Допустимые значения: "LQ", "MQ", "HQ".
 `user_agents`    | список | необязательный | Список User-Agent, которым можно / нельзя отдавать данный источник или поток.
 `recordable`     | булев  | необязательный | Флаг наличия записей телепередач для этого потока
 `aspect_ratio`   | строка | необязательный | Соотношение сторон для правильного отображения (растягивания/сужения) картинки, например, "16:9"
 `crop`           | строка | необязательный | Ширина:высота части кадра, которую необходимо гарантированно показать при кадрировании изображения, в процентах, например, "100:70"
 `has_timeshift`  | булев  | необязательный | Флаг поддержки источником технологии Timeshift
 `territory_id`   | число  | необязательный | ID территории Peers.TV
 `timeshift_url`  | строка | необязательный | URL для получения списка сегментов по технологии Timeshift. Обязателен, если `has_timeshift` = `True`
 `timeshift_header` | строка | необязательный | Заголовок, который необходимо отправлять при отдаче списка сегментов источника, который поддерживает timeshift. Если строка пуста или отсутствует, заголовок будет сгенерирован автоматически согласно шаблону из настроек HLS-AAA. Поддерживается макро: %(alias)s, %(stream_id)d, %(substream_id)d, %(session_id)s.
 `records_protected_path` | строка | необязательный | Полная аналогия `protected_path`, только для архива записей телепередач. Обязателен, если `recordable` = `True`.
 `crop_iptv` | строка | необязательный | По аналогии с `crop`, только в формате для IP-TV Player: обрезка кадра WxH+X+Y. Например, "690x550+15+10". Документация: http://borpas.info/iptvplayer-docs#16

Подробнее: [Protocol Buffers][p-streamsource]

#### Сообщение UserAgentRegexps <a id="m-useragentregexps"></a>

 параметр         | формат |     статус     | описание
------------------|--------|----------------|----------
 `regexp_list`    | список |  обязательный  | Регулярное выражение, поддерживаемое стандартным Python'овским модулем re: https://docs.python.org/2/library/re.html
 `type`           | число  |  обязательный  | Тип: INCLUDE (0) - отдавать только для указанных User-Agent'ов, EXCLUDE (1) - отдавать источник всем, кроме указанных User-Agent'ов

Подробнее: [Protocol Buffers](#m-useragentregexps)

#### Сообщение Category <a id="m-category"></a>

 параметр    | формат |     статус     | описание
-------------|--------|----------------|----------
 `title`     | строка |  обязательный  | при генерации списка каналов будет использовано в качестве названия категории
 `channels`  | список |  обязательный  | список идентификторов каналов, входящих в данную категорию
 
Подробнее: [Protocol Buffers](#m-category)

# Описания форматов способом Google Protocol Buffers

# ChannelList - список каналов и категорий <a id="p-channellist"></a>

    message ChannelList {
        required string title = 1;                     // Человекочитаемое название плейлиста
        repeated Channel channels = 2;
        repeated Category categories = 3;
        repeated Settings settings = 4;
    }

# Channel - описание канала <a id="p-channel"></a>

    message Channel {
        // Порядок сортировки каналов в выводе API будет использован для позиционирования части каналов, не попавших ни в одну категорию, в списке.
        required uint32 id = 1;                       // Единый постоянный идентификатор канала, совпадающий с использующимся RADIUS-сервером
        required string alias = 2;                    // Единый постоянный текстовый идентификатор канала
        required string title = 3;                    // Человекочитаемое название канала
        repeated StreamSource streams = 4;            // Источники вещания канала, обязательный параметр

        optional string identifier_url = 5;           // Ссылка на сущность (страница канала на сайте)
        optional string schedule_url = 6;             // Ссылка на программу телепередач
        optional string logo_url = 7;                 // Ссылка на логотип канала

        enum ChannelStatus {
            TESTING = 0;
            LAUNCHED = 1;
        }
         
        optional ChannelStatus status = 8;            // Статус канала: тестовое / боевое вещание
    }

# StreamSource - описание источника <a id="p-streamsource"></a>

    message StreamSource {
        required uint32 id = 1;                       // Постоянный идентификатор (например, порядковый номер) потока в рамках канала
        required string url = 2;                      // URL источника.
                                                      // Если тип источника = HLS_VARIANT:
                                                      // * Если передать пустую строку, URL будет автоматически сгенерирован согласно конфигурации HLS-AAA.
                                                      // * Настоятельно рекомендуется использование макроса "%(session_id)s", если дается ссылка на раздатчик HLS-AAA. Пример: http://hls.zomg.fqdn/masterindex/?sid=%(session_id)s

        optional string protected_path = 3;           // Путь для отдачи файлов (сегментов) через nginx по HTTP посредством X-Accel-Redirect.
                                                      // Это поле *требуется* для раздачи HLS, но совершенно бесполезно для потоков типа UDP|HLS_VARIANT|RAW.
                                                      // Требуется присутствие макроса "%(filename)s", который будет заменяться именем отдаваемого файла. Пример: "/protected/1kanal/tvrec/%(filename)s"

        enum StreamSourceType {
            HLS = 0;
            UDP = 1;
            HLS_VARIANT = 2;
            RAW = 3;                                  // Источник неподдерживаемого формата и/или без авторизации, адрес которого отдается "как есть". Тип на будущее, например, для HLS без ААА.
        }
     
        required StreamSourceType type = 4 [default = HLS];

        optional StreamSource substreams = 5;         // Максимально допустимый уровень вложенности: 1 (channel -> streams -> substreams)

        optional uint32 bandwidth = 6;                // Согласно стандарту HLS
        optional string resolution = 7;               // Согласно стандарту HLS
        optional string codecs = 8;                   // Согласно стандарту HLS
        optional string audio = 9;                    // Согласно стандарту HLS
        optional string name = 10;                    // Опциональный хак: LQ | MQ | HQ, подробнее: https://wiki.inetra.ru/pages/viewpage.action?pageId=13567356
     
        // Регулярные выражения должны поддерживаться стандартным Python'овским модулем re: https://docs.python.org/2/library/re.html
        optional UserAgentRegexps user_agents = 11;   // Список User-Agent'ов, которым можно/нельзя отдавать источник

        optional bool recordable = 12;                // Флаг наличия записей телепередач для этого потока
        optional string aspect_ratio = 13;            // Соотношение сторон для правильного отображения (растягивания/сужения) картинки, например, "16:9"
        optional string crop = 14;                    // Ширина:высота части кадра, которую необходимо гарантированно показать при кадрировании изображения, в процентах, например, "100:70"
        optional bool has_timeshift = 15;             // Флаг поддержки источником технологии Timeshift
        optional uint32 territory_id = 16;            // ID территории
        optional string timeshift_url = 17;           // URL для получения списка сегментов по технологии Timeshift. Обязателен, если has_timeshift=True. Требуется наличие макро %(program_id)s
        optional string timeshift_header = 18;        // Заголовок, который необходимо отправлять при отдаче списка сегментов источника, который поддерживает timeshift. Если строка пуста или отсутствует, заголовок будет сгенерирован автоматически согласно шаблону из настроек HLS-AAA. Поддерживается макро: %(alias)s, %(stream_id)d, %(substream_id)d, %(session_id)s
        optional string records_protected_path = 19;  // Полная аналогия `protected_path`, только для архива записей телепередач. Обязателен, если `recordable` = `True`. Требуется наличие макро %(date_time)s
        optional string crop_iptv = 20;               // По аналогии с `crop`, только в формате для IP-TV Player: обрезка кадра WxH+X+Y. Например, "690x550+15+10". Документация: http://borpas.info/iptvplayer-docs#16
    }

# UserAgentRegexps - набор регулярных выражений для фильтрации источников на основе User-Agent

    message UserAgentRegexps {
        repeated string regexp_list = 1;              // Обязательный параметр. Если регулярное выражение не валидно, оно будет отброшено.
     
        enum UserAgentRegexpType {
            INCLUDE = 0;                              // Отдавать источник только для указанных User-Agent'ов
            EXCLUDE = 1;                              // Отдавать источник всем, кроме указанных User-Agent'ов
        }
     
        required UserAgentRegexpType type = 2 [default = INCLUDE];
    }
    
# Category - описание категории каналов

    message Category {
        // Порядок сортировки будет использован для отображения каналов в плеере, см. https://wiki.videolan.org/XSPF/#VLC_Extensions
        required string title = 1;                     // Человекочитаемое название категории. Дублирующиеся категории будут объединены
        repeated uint32 channels = 2;                  // Список Channel ID. Список каналов каждой категории будет дедуплицирован, а несуществующие каналы - удалены.
    }
    
# Settings - различные настройки
    
    message Settings {
        optional UserAgentRegexps access_denied_channels_display_control = 1;   // Используется для перечисления User-Agent, которым можно/нельзя отдавать недоступные пользователю каналы.
    }

# Примеры использования

Запрос:

    GET /channels

Тело ответа:
    
    {
        "title": "Телевидение Электронного города",
        "channels":
        [
            {
                "id": 10338232,
                "alias": "vesti",
                "title": "Россия 24",
                "streams":
                [
                    {
                        "id": 0,
                        "url": "http:\/\/localhost\/remote_pls\/streaming\/vesti\/tvrec\/playlist.m3u8",
                        "protected_path": "\/protected\/streaming\/vesti\/tvrec\/%(filename)s",
                        "type": 0,
                        "bandwidth": 1024,
                        "resolution": "720x576",
                        "codecs": "avc.zomgwtf",
                        "recordable": true,
                        "has_timeshift": true,
                        "timeshift_url": "http:\/\/peers.tv\/timeshift\/vesti\/16\/playlist.m3u8?start_time=%(offset)s",
                        "timeshift_header": "base-uri="http:\/\/hls-aaa\/timeshift\/vesti\/playlist.m3u8";duration=3600",
                    },
                    {
                        "id": 1,
                        "url": "udp:\/\/@239.1.15.3:1234",
                        "type": 1,
                        "bandwidth": 1024,
                        "resolution": "720x576",
                        "codecs": "avc.qwerty",
                        "recordable": false,
                        "has_timeshift": false,
                        "user_agents":
                        {
                            "regexp_list":
                            [
                                "^.*$",
                                "samsung",
                                "smarttv",
                                "^eltex"
                            ],
                            "type": 0
                        }
                    }
                ],
                "identifier_url": "http:\/\/www.cn.ru\/entities\/10338232\/",
                "schedule_url": "http:\/\/www.cn.ru\/tv\/program\/vesti",
                "logo_url": "http:\/\/www.cn.ru\/data\/illustrations\/ills\/2013\/08\/01\/24493\/24493963.png",
                "status": 1,
                "territory_id": 17
            }
        ],
        "categories":
        [
            {
                "title": "Эфир",
                "channels": [10338245, 10338232]
            },
            {
                "title": "Познавательный",
                "channels": [10338246]
            }
        ],
        "settings":
        [
            "access_denied_channels_display_control":
            {
                "regexp_list":
                [
                    "^.*$"
                ],
                "type": 1
            }
        ]
    }

[m-streamsource]: #m-streamsource
[p-channel]: #p-channel
[p-channellist]: #p-channellist
[p-streamsource]: #p-streamsource

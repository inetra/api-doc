title: Launcher API
quotes language: french
version: 1.2
status: 

# Введение

Данный сервис предназначен для получения сущности Афиши для лаунчера.  Это такие сущности, как:
   - выпуск передачи (id канала, id выпуска передачи)
   - фильм (id фильма)
   -  канал (id канала)

# Размещение и использование

Точка входа определяется [Регистратурой][registry-api-ref], при этом числовой идентификатор сервиса — `20`, строковый — `launcher`.

Запросы формируются следующим образом:

[registry-api-ref]: registry.md

	http://<path_to_api>/<api_version>/<method>.<format>?[parameters]

Где:

- `path_to_api` — путь до API, полученный из Регистратуры
- `api_version` — версия API 
- `method` — имя метода
- `format` — формат передачи данных, может быть одним из:
	- `json` — JSON
	- `xml` — XML
- `parameters` — параметры метода

Значения всех параметров необходимо кодировать для предотвращения неоднозначной интерпретации так, как это рекомендуется в [RFC3986].

[RFC3986]: http://tools.ietf.org/html/rfc3986

	
# Методы Launcher API
## `posters` — получение списка афиш для лаунчера, которые добавлены в блок "Афиши лаунчера"
Формат ответа: сообщение [`PosterList`][posters-list-message].

Пример запроса:

	GET /launcher/1/posters.json

## `poster` — получение информации об афишах в подборке и о связанных афишах
Формат ответа: сообщение [`Poster`][poster-message].

Пример запроса:

	GET /launcher/1/poster.json?<id>	

 параметр | значение
----------|----------
`id`      | идентификатор подборки (коллекции)

Замечания:
Методам можно передать GET параметр `moderation` со значением `true`, в этом случае API вернёт афиши помеченные для премодерации. Это параметр не должен использоваться в публичной версии приложений.

# Форматы сообщений
## PosterList — вывод списка афиш лаунчера [posters-list-message]

	message PosterList {
      repeated Poster posters = 1;
	}	
	
## Poster — информация об афише лаунчера [poster-message]	
	message Poster {
      enum PosterType {
	    FILM = 0;
	    TELECAST = 1;
	    CHANNEL = 2;
	    YOUTUBE = 3;
	    NOTIFICATION = 4;
	    COLLECTION = 5;
	    VOD = 6;
      }	

	  optional uint64 id = 1;
	  optional PosterType type = 2;
	  optional string title = 3;
	  repeated LauncherImg images = 4;
	  optional string color = 5;
	  optional uint32 channel_id = 6;
	  optional uint32 telecast_id = 7;
	  optional uint32 film_id = 8;
	  optional string description = 9;
	  optional uint32 duration = 10;
	  optional bool is_promo = 11;
	  optional string youtube_id = 12;
	  optional string link = 13;
	  repeated Poster attached_posters = 14;
	  repeated Poster related_posters = 15;
	  optional uint32 vod_id = 16;
	}  
	
Замечания:

- `id` — идентификатор афиши  в блоке "Афиши лаунчера"
- `type ` — тип постера: 
 	- `Film` — фильм;
	- `Telecast` — выпуск передачи;
	- `Channel` — канал;
	- `Collection` — коллекция фильмов или телепередач;
	- `Youtube` — ролик youtube;
	- `Notification` — пуш-уведомления;
	- `VOD` — VOD-контент;
- `title` — название фильма/передачи/канала;
- `color` — цвет "подложки" афиши, закодирован в hex;
- `channel_id` — идентификатор канала;
- `telecast_id` — идентификатор выпуска передачи;
- `film_id` — идентификатор фильма:
- `youtube_id` — идентификатор ролика youtube;
- `description` — описание фильма/передачи:
- `duration` — длительность передачи/фильма;
- `is_promo` — метка промо;
- `link` — ссылка на афишу (на ролик youtube). Вводится моедратором в админке;
- `attached_posters` — вывод афиш, входящих в подборку;
- `related_posters` — вывод связанных афиш.

## LauncherImg — информация об иллюстрации афиши лаунчера  [launcherImg-message]

	message LauncherImg {
      optional string url = 1;
	  optional uint32 width = 2;
      optional uint32 height = 3;
      optional string profile = 4;
	}

Замечания:

- `url` - ссылка на иллюстрацию афиши
- `width` - ширина иллюстрации
- `height` - высота иллюстрации
- `profile` - тип профиля иллюстрации (может быть 'vertical', 'horizontal', либо 'promo')

# История версий

## Версия 1.0

Начальная версия (WEBDEV-12377)

- описан метод лаунчера `posters`;
- описан метод лаунчера `poster` c обязательным параметром `id`;

## Версия 1.1
Премодерация (PTVIOS-2012)

- описана возможность запросить неактивные афиши, помеченные признаком для премодерации.

## Версия 1.2

- добавлен тип VOD в сообщение [`Poster`][poster-message].

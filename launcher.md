title: Launcher API
quotes language: french
version: 1
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
	}  
	
Замечания:

- `poster_id` — идентификатор афишы  в блоке "Афишы лаунчера"
- `type ` — тип постера: 
 	- `Film` — фильм;
	- `Telecast` — выпуск передачи;
	- `Channel` — канал.
- `title` — название фильма/передачи/канала;
- `color` — цвет "подложки" афиши, закодирован в hex;
- `channel_id` — идентификатор канала;
- `telecast_id` — идентификатор выпуска передачи;
- `film_id` — идентификатор фильма:
- `description` — описание фильма/передачи:
- `duration` — длительность передачи/фильма. 
- `is_promo` — метка промо.   

## LauncherImg — информация об иллюстрации афиши лаунчера  [launcherImg-message]

	message LauncherImg {
      optional string url = 1;
	  optional uint32 width = 2;
      optional uint32 height = 3;
      optional string profile = 4.
	  }	

Замечания:

- `url` - ссылка на иллюстрацию афиши
- `width` - ширина иллюстрации
- `height` - высота иллюстрации
- `profile` - тип профиля иллюстрации (может быть 'vertical', 'horizontal', либо 'promo')

# История версий

## Версия 1.0

Начальная версия (WEBDEV-12377)
	
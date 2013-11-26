title: Playlist extending rules
version: 0.3.0
status: в разработке

# Правила расширения плейлистов

Данный документ описывает правила расширения плейлистов формата M3U и XSPF для поддержки расширенных атрибутов при описании списка каналов.

## Общее описание

Основной целью расширения форматов плейлистов является внесение дополнительной информации, способной улучшить взаимодействие пользователя с приложением.

Плейлист может быть расширен на двух уровнях:

- на уровне плейлиста. В этом случае расширение может применяться как к плейлисту, так и ко всем элементам плейлиста.
- на уровне элемента плейлиста. Расширение применяется только к элементу.

Расширение плейлиста на затрагивает совместимость с большинством известных проигрывателей, таких как VLC, и должно соответствовать известным стандартам.

### Атрибуты каналов

- Идентификатор канала(доступен в [TV Guide API](tv-guide.md))
- Признак наличия записей
- Признак доступности канала: `allowed`, `forbidden`, `payable`
- Разрешение источника: `SD`, `HD`, `FullHD`, `4D`, 720x576
- Соотношение сторон: 4:3, 16:9, 16:10
- Признак потока: только аудио.

### Версионирование

Существующие расширения плейлистов подразумеваются первой версией, при этом версия явно указываться не должна.[^fn-versioning] 

### Интеграция со сторонними системами генерации плейлистов

При обращении за плейлистом рекомендуется устанавливать HTTP-заголовок `User-Agent` . Данный заголовок может быть использован при генерации плейлиста. Значение заголовка должно однозначно определять платформу и класс устройства.

Пример задания заголовка `User-Agent`

	Peers.TV/3.2.1 (iOS/3.2.1; iPad/5,1;) Darwin/14.0.0

### Рекомендации для поставщиков услуги IPTV

При реализации системы ограничения доступа к плейлисту, например, только для своих абонентов, при обращении к плейлисту для неабонентов сети рекомендуется возвращать пустой плейлист со кодом 200 HTTP-статуса.


# Формат M3U

Расширение плейлиста осуществляется на основании возможности включения комментариев и произвольных директив, начинающиеся со символа "#"

**Mime-type**: audio/x-mpegurl

## Директивы:

- EXTINF
- EXT-CN-VERSION
- EXT-CN-CHANNEL-INFO
- EXT-CN-STREAM-INFO

### EXTINF

Описывает длительность и название элемента плейлиста.

название     | по умолчанию | смысл
-------------|--------------|-------------
`cn-id`      | 0            | Идентификатор канала, доступен в [TV Guide API](tv-guide.md) (<span style="color:#f00">Устарело в версии 2</span>)

### EXT-CN-VERSION

Данная директива задает версию плейлиста. Если не указана, то подразумевается версия 1.

### EXT-CN-CHANNEL-INFO

Директива описывает информацию о канале. Доступна с версии 2.

Параметры:

   название  | по умолчанию | смысл
-------------|--------------|-------------
`channel-id` | `0`          | Идентификатор канала(доступен в [TV Guide API](tv-guide.md))
`access`     | `allowed`    | Условия доступа к каналу
`recordable` | `false`      | Наличие записей для данного канала

Значения параметра `access`:

- `allowed`. Канал доступен для просмотра.
- `forbidden`. Доступ к каналу запрещен.
- `payable`. На канал может быть оформлена подписка.


### EXT-CN-STREAM-INFO

Директива описывает свойства медиа-потока. Доступна с версии 2.

Параметры

название      | по умолчанию | смысл
--------------|--------------|-------------
`definition ` | отсутствует  | Идентифицирует разрешение источника.
`aspect-ratio`| отсутствует  | Идентифицирует соотношение сторон, например 4:3.
`audio-only`  | `false`      | Идентифицирует отсутствие видео-дорожке в потоке

Параметр `definition` может быть задан:

- константой: SD, HD, FullHD, 4D
- в формате `ширина` x `высота`. 720x576

## Примеры формирования плейлиста

### Версия 2
	#EXTM3U
	#EXT-CN-VERSION:2
	
	#EXTINF:-1, Первый канал
	#EXT-CN-CHANNEL-INFO: channel-id=10338245 access=allowed recordable=true
	#EXT-CN-STREAM-INFO: definition=SD aspect-ratio=4:3
	udp://@239.1.15.1:1234

	#EXTINF:-1, Россия 1
	#EXT-CN-CHANNEL-INFO: channel-id=10338258 access=allowed
	udp://@239.1.15.2:1234

### Версия 1
	#EXTM3U
	#EXTINF:-1 cn-id=10338245 group-title="Эфир", Первый канал
	udp://@239.1.15.1:1234
	#EXTINF:-1 cn-id=10338258, Россия 1
	udp://@239.1.15.2:1234



# Формат XSPF

Расширение плейлиста осуществляется на основе документации [стандарта XSPF](http://www.xspf.org/xspf-v1.html).

**Mime-type**: application/xspf+xml

## Теги

- cn:channel-id
- cn:version
- cn:access
- cn:definition
- cn:aspect-ratio
- cn:audio-only
- cn:recordable

### Устаревшие теги

Версия 1:

- cn:id
- cn:link
- cn:records
- cn:location

Расширение для приставок Eltex:

- cn:tv-channel-definition
- cn:tv-channel-status
- cn:tv-channel-subscription


## Примеры формирования плейлиста

### Версия 2[^fn-vlc-support]

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<extension application="http://www.cn.ru">
			<cn:version>2</cn:version>
		</extension>
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>http://hls.cn.ru/streaming/1kanal/tvrec/playlist.m3u8</location>
				<title>Первый</title>
				<extension application="http://www.cn.ru">
					<cn:channel-id>10338245</cn:channel-id>
					<cn:recordable>true</cn:recordable>
					<cn:access>allowed</cn:access>
					<cn:definition>SD</cn:definition>
				</extension>
			</track>
			<track>
				<location>udp://@239.1.15.2:1234</location>
				<title>Россия 1</title>
				<extension application="http://www.cn.ru">
					<cn:channel-id> 10338258</cn:channel-id>
					<cn:recordable>false</cn:recordable>
					<cn:access>forbidden</cn:access>
					<cn:definition>SD</cn:definition>
				</extension>
			</track>
		</trackList>
	</playlist>

### Версия 1

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>udp://@239.1.15.1:1234</location>
				<title>Первый</title>
				<extension application="http://www.cn.ru">
					<cn:id>10338245</cn:id>
					<cn:link>http://www.cn.ru/tv/program/1kanal/</cn:link>
					<cn:records>1</cn:records>
					<cn:location type="hls">http://hls.cn.ru/streaming/1kanal/tvrec/playlist.m3u8</cn:location>
				</extension>
			</track>
		</trackList>
	</playlist>

### Версия 1 (Eltex)

	<?xml version="1.0" encoding="UTF-8"?>
		<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>udp://@239.1.10.23:1234</location>
				<title>Первый HD</title>
				<image>http://www.cn.ru/data/illustrations/ills/2013/08/01/24494/24494403.png</image>
				<psfile>2812</psfile>
				<extension application="http://www.cn.ru/">
					<cn:id>21381677</cn:id>
					<cn:tv-channel-definition>HD</cn:tv-channel-definition>
					<cn:tv-channel-status>LAUNCHED</cn:tv-channel-status>
					<cn:tv-channel-subscription>SUBSCRIBED</cn:tv-channel-subscription>
				</extension>
			</track>
		</trackList>
	</playlist>


TODO:

- описать расширение плейлиста;
- Описать расширение элемента плейлиста для версий 1 и 2;
- Заменить домен cn, чтобы избежать возможных коллизий.


[^fn-vlc-support]: По неизвестной причине плеер VLC не поддерживает описание расширения тега playlist в начале плейлиста, но с точки зрения реализации это был бы правильный выбор. Для совместимости с уже выпущенными версиями необходимо рассмотреть возможность описания расширений тега playlist в конце плейлиста.
[^fn-versioning]: Уточнить что имеется ввиду под "существующими" версиями. Описать совместимость между версиями.


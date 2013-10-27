title: Playlist extending rules
version: 0.1.0
status: в разработке

# Правила расширения плейлистов

Плейлист и любой элемент плейлиста может содержать служебную информацию.
Плейлист должен соответствовать стандарту и как следствие должен быть непротиворечивым и совместимым со сторонними плеерами.

Данный документ описывает правила расширения плейлистов формата M3U и XSPF для поддержки расширенных атрибутов при описании списка каналов.

Атрибуты каналов:

- Идентификатор канала(доступен в [TV Guide API](tv-guide.md))
- Признак наличия записей
- Признак доступности канала: allowed, forbidden, payable
- Тип источника: HLS, Multicast
- Разрешение источника: SD, HD, FullHD, 4D
- Соотношение сторон: 4:3, 16:9, 16:10

Существующие расширения плейлистов подразумеваются первой версией, при этом версия явно указываться не должна.

ТОDO:

- подумать над передачей HTTP-заголовка с рекомендацией о формировании плейлиста, например, передавая название профиля и/или тип устройства. Абстрактный пример заголовка: **CN-Supported-Profile: mobile-1203fn**

# Формат M3U

Расширение плейлиста осуществляется на основании возможности включения комментариев и произвольных директив, начинающиеся со символа "#"

**Mime-type**: audio/x-mpegurl

### Директивы:

- EXT-CN-VERSION
- EXT-CN-CHANNEL-INFO
- EXT-CN-STREAM-INFO


Пример указания идентификатора канала в плейлисте(<span style="color:#f00">Устарело в версии 2</span>):

	#EXTM3U
	#EXTINF:-1 cn-id=10338245 group-title="Эфир", Первый канал
	udp://@239.1.15.1:1234
	#EXTINF:-1 cn-id=10338258, Россия 1
	udp://@239.1.15.2:1234

Пример, сформированного плейлиста в формате M3U(версия 2) 

	#EXTM3U
	#EXT-CN-VERSION:2
	
	#EXTINF:-1 group-title="Эфир", Первый канал
	#EXT-CN-CHANNEL-INFO: channel-id=10338245 access=allowed recordable=true
	#EXT-CN-STREAM-INFO: definition=SD type=multicast aspect-ratio=4:3
	udp://@239.1.15.1:1234

	#EXTINF:-1 cn-id=10338258, Россия 1
	#EXT-CN-CHANNEL-INFO: channel-id= 10338258 access=allowed
	udp://@239.1.15.2:1234

TODO:

- Описать директивы и атрибуты(значения по умолчанию, если атрибут отсутствует)
- Описать версию 1



# Формат XSPF

Расширение плейлиста осуществляется на основе документации [стандарта XSPF](http://www.xspf.org/xspf-v1.html).

**Mime-type**: application/xspf+xml

### Теги
- cn:version
- cn:channel-id
- cn:access
- cn:definition
- cn:stream-type
- cn:recordable

Пример  XSPF-плейлиста с указанием идентификатора канала(<span style="color:#f00">Устарело в версии 2</span>):

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>udp://@239.1.15.1:1234</location>
				<title>Первый</title>
				<extension application="http://www.cn.ru">
					<cn:id>10338245</cn:id>
				</extension>
			</track>
			<track>
				<location>udp://@239.1.15.2:1234</location>
				<title>Россия 1</title>
				<extension application="http://www.cn.ru">
					<cn:id>10338258</cn:id>
				</extension>
			</track>
		</trackList>
	</playlist>


Пример, сформированного плейлиста в формате XSPF(версия 2) :

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<extension application="http://www.cn.ru">
			<cn:version>2</cn:version>
		</extension>
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>udp://@239.1.15.1:1234</location>
				<title>Первый</title>
				<extension application="http://www.cn.ru">
					<cn:channel-id>10338245</cn:channel-id>
					<cn:access>allowed</cn:access>
					<cn:definition>SD</cn:definition>
					<cn:stream-type>multicast</cn:stream-type>
				</extension>
			</track>
			<track>
				<location>udp://@239.1.15.2:1234</location>
				<title>Россия 1</title>
				<extension application="http://www.cn.ru">
					<cn:channel-id> 10338258</cn:channel-id>
					<cn:access>forbidden</cn:access>
					<cn:definition>SD</cn:definition>
					<cn:stream-type>multicast</cn:stream-type>
				</extension>
			</track>
		</trackList>
	</playlist>


TODO:

- описать расширение плейлиста[^fn-vlc-support]
- Описать расширение элемента плейлиста
- Описать теги, используемые в первой версии
- Разобраться с доменами тегов(cn:id)
- Заменить домен cn, чтобы избежать возможных коллизий


[^fn-vlc-support]: По неизвестной причине плеер VLC не поддерживает описание расширения тега playlist в начале плейлиста, но с точки зрения реализации это был бы правильный выбор. Для совместимости с уже выпущенными версиями возможно рассмотреть возможность описания расширений тега playlist вконце плейлиста


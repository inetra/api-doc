title: Правила расширения форматa XSPF
version: 0.13.0
status: RC4
jira-ticket: TVREC-70
jira-ticket: TVREC-175

# Общее описание

Данный документ описывает правила расширения форматa XSPF для внесения дополнительной информации (директив), способной улучшить взаимодействие пользователя с приложением, при описании списка каналов (плейлиста).

Документ предназначен для разработчиков приложений и поставщиков услуг IPTV–вещания, записей телепередач.

Расширение форматов не затрагивает совместимость с большинством известных проигрывателей, таких как VLC, и соответствует существующим стандартам.

При формировании списка каналов должна использоваться кодировка UTF–8.

## Атрибуты каналов

- Идентификатор канала (доступен в [TV Guide API][tv-guide-api]);
- Признак наличия архива записей телепередач.

Архив записей телепередач предоставляется при помощи [TV Guide API][tv-guide-api] и [MediaLocator API][media-locator-api]. Признак наличия архива не гарантирует доступность записей для конечного пользователя.

[tv-guide-api]: tv-guide.md
[media-locator-api]: media-locator.md

# Формат XSPF

Расширение формата осуществляется на основе документации [стандарта XSPF](http://www.xspf.org/xspf-v1.html). Расширение содержит набор директив, находящихся в пространстве имен `cn`, и атрибутов к ним. Пространство имен должно быть указано соответствующим параметром в свойствах корневого элемента `playlist` формата XSPF.

Пример задания пространства имен `cn`:

	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">

**Mime-type**: application/xspf+xml

## Расширение формата

Для указания дополнительной информации могут быть добавлены дополнительные директивы с использованием механизма расширения формата XSPF (см. [стандарт XSPF](http://www.xspf.org/xspf-v1.html)).

*Запрещается* использовать пространства имен `cn` и `inetra`.

## Директивы

Каждая директива может содержать значение или набор атрибутов, атрибуты указываются в виде вложенных элементов.

Ниже приведены соглашения по интерпретации типов данных атрибутов:

тип данных | примечания
-----------|------------
`число`    | числовое предоставление
`дробное`  | дробная часть отделяется точкой
`строка`   | символьное представление строки

Строковые атрибуты должны быть закодированы в соответствии со [спецификацией XML][xml-specification]

[xml-specification]: http://www.w3.org/TR/xml11/#sec-well-formed

**Основные директивы**:

- cn:id
- cn:link
- cn:records
- cn:location

**Дополнительные директивы для приставок Eltex–Linux**:

- cn:tv-channel-definition
- cn:tv-channel-status
- cn:tv-channel-subscription

### cn:id

Директива содержит информацию об идентификаторе канала в сервисе [TV Guide API](tv-guide.md).

### cn:link

Директива содержит ссылку на программу телепередач для данного канала.

### cn:records

Директива описывает признак наличия записей для канала.

Принимает значения:

- `0` – отсутствуют записи для канала;
- `1` - присутствуют записи для канала.

### cn:location

Директива описывает альтернативные источники для вещания, в свойствах директивы при помощи параметра `type` дополнительно указывается тип вещания.

Известные типы вещания:

- `hls` — вещание осуществляется по протоколу HTTP Live Streaming.

### cn:tv-channel-definition

Директива описывает разрешение источника вещания.

Разрешение может быть задано константой:

- `SD` — стандартная чёткость;
- `HD` — высокая чёткость.

### cn:tv-channel-status

Директива описывает статус канала.

Возможные статусы канала:

- `TESTING ` — канал в тестовом вещании;
- `LAUNCHED` — канал "в бою", продаётся.

### cn:tv-channel-subscription

Директива содержит информацию о подписке на канал.

Возможные значения:

- `NOT_SUBSCRIBED ` — подписки нет, но подписаться можно;
- `SUBSCRIPTION_PENDING ` — подписка есть, идёт применение подписки к оборудованию;
- `SUBSCRIBED ` — подписка есть, применена к оборудованию.

## Примеры формирования плейлиста

**С основными директивами**:

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

**С дополнительными директивами для приставок Eltex ("Электронный Город")**:

	<?xml version="1.0" encoding="UTF-8"?>
		<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">
		<title>Телевидение Электронного города</title>
		<trackList>
			<track>
				<location>udp://@239.1.10.23:1234</location>
				<title>Первый HD</title>
				<image>http://www.cn.ru/data/illustrations/ills/2013/08/01/24494/24494403.png</image>
				<extension application="http://www.cn.ru/">
					<cn:id>21381677</cn:id>
					<cn:tv-channel-definition>HD</cn:tv-channel-definition>
					<cn:tv-channel-status>LAUNCHED</cn:tv-channel-status>
					<cn:tv-channel-subscription>SUBSCRIBED</cn:tv-channel-subscription>
				</extension>
			</track>
		</trackList>
	</playlist>

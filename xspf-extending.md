title: Правила расширения форматa XSPF
version: 0.13.0
status: RC5
jira-ticket: TVREC-70
jira-ticket: TVREC-175

# Общее описание

Данный документ описывает правила расширения форматa XSPF для внесения дополнительной информации (директив), способной улучшить взаимодействие пользователя с приложением, при описании списка каналов (плейлиста).

Документ предназначен для разработчиков приложений и поставщиков услуг IPTV–вещания, записей телепередач.

Расширение форматов не затрагивает совместимость с большинством известных проигрывателей, таких как VLC, и соответствует существующим стандартам.

При формировании списка каналов должна использоваться кодировка UTF–8.

## Атрибуты каналов

- Идентификатор канала (доступен в [TV Guide API][tv-guide-api]);
- Признак наличия архива записей телепередач;
- Разрешение видео–потока источника;
- Признак наличия доступа к каналу: доступен для просмотра, доступ запрещен.

Архив записей телепередач предоставляется при помощи [TV Guide API][tv-guide-api] и [MediaLocator API][media-locator-api]. Признак наличия архива не гарантирует доступность записей для конечного пользователя.

[tv-guide-api]: tv-guide.md
[media-locator-api]: media-locator.md

# Формат XSPF

Расширение формата осуществляется на основе документации [стандарта XSPF](http://www.xspf.org/xspf-v1.html). Расширение содержит набор директив, находящихся в пространстве имен `cn`, и атрибутов к ним. Пространство имен должно быть указано соответствующим параметром в свойствах корневого элемента `playlist` формата XSPF.

Пример задания пространства имен `cn`:

	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">

**Mime-type**: application/xspf+xml

## Версионирование

Версионирование расширений осуществляется путем добавления специальной директивы. Если версия не указана явно, то подразумевается первая версия.

Версия указывает на минимально поддерживаемую версию расширения. Клиенты могут распознавать директивы старшей, чем указано, версии, если отсутствует явное требование к минимальной версии расширения для данных директив.

Таким образом, возможно сформировать список каналов, совместимый с первой и второй версией расширения одновременно.

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
`булев`    | принимает два значения `true` или `false`

Строковые атрибуты должны быть закодированы в соответствии со [спецификацией XML][xml-specification]

[xml-specification]: http://www.w3.org/TR/xml11/#sec-well-formed

**Версия 2**:

- inetra:version
- inetra:channel-inf
- inetra:stream-inf

**Версия 1**:

- cn:id
- cn:link
- cn:records
- cn:location

**Дополнительные директивы для приставок Eltex–Linux**:

- cn:tv-channel-definition
- cn:tv-channel-status
- cn:tv-channel-subscription

### inetra:version

Директива задает версию расширения. Доступна с версии 2. Указывается на уровне плейлиста.

### inetra:channel-inf

Директива описывает информацию о канале. Появилась в версии 2.

Дополнительные параметры:

название      | тип    | по умолчанию | смысл
--------------|--------|--------------|-------------
`channel-id`  |`число` | `0`          | Идентификатор канала(доступен в [TV Guide API](tv-guide.md))
`territory-id`|`число` | отсутствует  | Идентификатор территории (доступен в [Registry API][registry-api])
`recordable`  |`булев` | `false`      | Наличие архива записей телепередач для данного канала
`allowed`     |`булев` | `true`       | Признак наличия доступа к каналу

Идентификатор территории `territory-id` описывает регион, для которого осуществляется вещание:

- если регион вещания не указан, то подразумевает текущий регион;
- указывать регион необходимо только для каналов, имеющих несколько сеток вещания, в том случае если нельзя гарантировать, что пользователь получит источник вещания для его региона.

[registry-api]: registry.md

### inetra:stream-inf

Директива описывает свойства медиа–потока. Появилась в версии 2.

Дополнительные параметры:

название      | тип    | по умолчанию | смысл
--------------|--------|--------------|-------------
`resolution ` |`строка`| отсутствует  | Идентифицирует разрешение источника.

Параметр  `resolution` должен быть задан в формате `ширина` x `высота`, например `720`x`576`.

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

**Версия 2**:

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:inetra="http://www.inetra.ru">
	<extension application="http://www.inetra.ru">
	    <inetra:version>2</inetra:version>
	</extension>
	<title>Телевидение Электронного города</title>
	<trackList>
	    <track>
	        <location>http://hls.cn.ru/streaming/1kanal/tvrec/playlist.m3u8</location>
	        <title>Первый</title>
	        <extension application="http://www.inetra.ru">
	            <inetra:channel-inf>
	               <channel-id>10338245</channel-id>
	               <recordable>true</recordable>
	            </inetra:channel-inf>
	            <inetra:stream-inf>
	               <resolution>720x576</resolution>
	            </inetra:stream-inf>
	        </extension>
	    </track>
	    <track>
	        <location>udp://@239.1.15.2:1234</location>
	        <title>Россия 1</title>
	        <extension application="http://www.inetra.ru">
	            <inetra:channel-inf>
	               <channel-id>10338258</channel-id>
	               <recordable>false</recordable>
	               <allowed>false</allowed>
	            </inetra:channel-inf>
	            <inetra:stream-inf>
	               <resolution>720x576</resolution>
	            </inetra:stream-inf>
	        </extension>
	    </track>
	</trackList>
	</playlist>

**Версия 1**:

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

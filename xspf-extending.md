title: Правила расширения форматa XSPF
version: 3.2.0
status: согласован

# Общее описание

Данный документ описывает правила расширения форматa XSPF для внесения дополнительной информации (директив), способной улучшить взаимодействие пользователя с приложением, при описании списка каналов (плейлиста).

Документ предназначен для разработчиков приложений и поставщиков услуг IPTV–вещания, записей телепередач.

Расширение форматов не затрагивает совместимость с большинством известных проигрывателей, таких как VLC, и соответствует существующим стандартам.

При формировании списка каналов должна использоваться кодировка UTF–8.

Детальное описание принципов формирования списка доступных каналов отражено в разделе [«Список каналов»][iptv-channel-list].

[iptv-channel-list]: iptv.md?id=iptv-1.3.2#channels-list

# Формат XSPF

XSPF — особое расширение XML, предназначенное для описания плейлиста, формат описан в официальной документации [стандарта XSPF](http://www.xspf.org/xspf-v1.html).

**Mime-type**: application/xspf+xml

## Версионирование

Версионирование расширений осуществляется путем добавления специальной директивы. Если версия не указана явно, то подразумевается первая версия.

Версия указывает на минимально поддерживаемую версию расширения. Клиенты могут распознавать директивы старшей, чем указано, версии, если отсутствует явное требование к минимальной версии расширения для данных директив.

Таким образом, возможно сформировать список каналов, совместимый с первой и второй версией расширения одновременно.

## Расширение формата

Для указания дополнительной информации могут быть добавлены дополнительные директивы с использованием механизма расширения формата XSPF (см. [стандарт XSPF](http://www.xspf.org/xspf-v1.html)).

*Запрещается* использовать пространства имен `cn` и `inetra`.

## Директивы

Директивы указываются в специальных блоках `extension` и могут быть описаны на уровне плейлиста или элемента. Каждая директива принадлежит к пространству имен `cn` или `inetra` и содержит значение или набор атрибутов в виде вложенных элементов. Пространство имен должно быть указано соответствующим параметром в свойствах корневого элемента `playlist` формата XSPF.

Пример задания пространства имен `cn`:

	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:cn="http://www.cn.ru">

Пример задания пространства имен `inetra`:

	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:inetra ="http://www.inetra.ru">

Пример задания пространств имен `inetra` и `vlc`:

	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" xmlns:inetra ="http://www.inetra.ru">

Ниже приведены соглашения по интерпретации типов данных атрибутов:

тип данных | примечания
-----------|------------
`число`    | числовое представление
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

Директива задает версию расширения. Доступна в версии 2. Указывается на уровне плейлиста.

### inetra:channel-inf

Директива описывает информацию о канале. Появилась в версии 2.

Дополнительные атрибуты:

название      | тип    | по умолчанию | смысл
--------------|--------|--------------|-------------
`channel-id`  |`число` | отсутствует  | Идентификатор канала(доступен в [TV Guide API](tv-guide.md))
`territory-id`|`число` | отсутствует  | Идентификатор территории (доступен в [Registry API][registry-api])
`recordable`  |`булев` | `false`      | Наличие архива записей телепередач для данного канала
`allowed`     |`булев` | `true`       | Признак наличия доступа к каналу (<span style="color:#f00">устарел в версии 3</span>)
`age-restriction`|`число`|отсутствует | Возрастное ограничение для канала

Идентификатор территории `territory-id` описывает регион, для которого осуществляется вещание:

- если регион вещания не указан, то подразумевает текущий регион;
- указывать регион необходимо только для каналов, имеющих несколько сеток вещания, в том случае если нельзя гарантировать, что пользователь получит источник вещания для его региона.

[registry-api]: registry.md

Возрастное ограничение задает минимально разрешенный возраст для просмотра канала.

### inetra:stream-inf

Директива описывает свойства медиа–потока. Появилась в версии 2.

Дополнительные атрибуты:

название       | тип    | по умолчанию | смысл
---------------|--------|--------------|-------------
`resolution`   |`строка`| отсутствует  | Идентифицирует разрешение источника
`aspect-ratio` |`строка`| отсутствует  | Соотношение сторон кадра
`crop`         |`строка`| отсутствует  | Кадрирование изображения
`has-timeshift`|`булев` | `false`      | Признак наличия поддержки [технологии Timeshift][timeshift-anchor]
`access`       |`строка`| `allowed`    | Наличие доступа к источнику вещания канала
`pending-till` |`число` | отсутствует  | Время планируемого появления доступа к вещанию канала у абонента
`allowed-till` |`число` | отсутствует  | Время планируемого отключения доступа к вещанию канала у абонента

Атрибут  `resolution` должен быть задан в формате `ширина` x `высота`, например, `720x576`:

- указание разрешения источника в виде `0x0` обозначает отсутствие видео–дорожки в потоке;
- в случае вариативного вещания список разрешений источника может быть указан перечислением через запятую.

Принципы использования атрибутов `access`, `allowed-till` и `pending-till` описаны в разделе [Взаимодействие с автоматизированной системой расчетов оператора связи][iptv-billing-communicate].

Атрибуты `aspect-ratio` и `crop` указываются в формате `ширина` : `высота`, например: `1:1`, `16:9`. Кадрирование изображения производится после изменения соотношения сторон (если оно есть). Порядок их использования описан в разделе [Кадрирование и изменение пропорций изображений каналов стандартной четкости][iptv-crop-n-aspect-ratio].

Признак наличия поддержки технологии Timeshift `has-timeshift` носит вспомогательный характер и не гарантирует поддержку сервером вещания.

[iptv-billing-communicate]: iptv.md?id=iptv-1.3.2#billing-communicate
[iptv-crop-n-aspect-ratio]: iptv.md?id=iptv-1.3.2#crop-n-aspect-ratio
[timeshift-anchor]: iptv.md?id=iptv-1.3.2#timeshift

### cn:id

Директива содержит информацию об идентификаторе канала в сервисе [TV Guide API](tv-guide.md).

### cn:link

Директива содержит ссылку на программу телепередач для данного канала.

### cn:records

Директива описывает признак наличия записей для канала.

Принимает значения:

- `0` – отсутствуют записи для канала;
- `1` - присутствуют записи для канала.

### cn:location (<span style="color:#f00">Устарело</span>)

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

### Поддерживаемые директивы пространства имен vlc

### vlc:id

Директива содержит целочисленный идентификатор канала, используется для группировки.

### vlc:node

Директива задает группировку каналов. Состоит из элементов `vlc:item`. Указывается на уровне плейлиста.

Дополнительные параметры:

название      | тип    | по умолчанию | смысл
--------------|--------|--------------|-------------
`title`       |`строка`| отсутствует  | Название группы каналов

#### vlc:item

Дополнительные параметры:

название      | тип    | по умолчанию | смысл
--------------|--------|--------------|-------------
`tid`         |`число` | отсутствует  | Идентификатор канала, заданный параметром `vlc:id`


## Примеры формирования плейлиста

**Версия 3**:

	<?xml version="1.0" encoding="UTF-8"?>
	<playlist version="1" xmlns="http://xspf.org/ns/0/" xmlns:inetra="http://www.inetra.ru" xmlns:vlc="http://www.videolan.org/vlc/playlist/0">
	<extension application="http://www.inetra.ru">
	    <inetra:version>3</inetra:version>
	</extension>
	<extension application="http://www.videolan.org/vlc/playlist/0">
	    <vlc:node title="Эфир">
	        <vlc:item tid="0" />
	        <vlc:item tid="1" />
	    </vlc:node>
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
	               <aspect-ratio>4:3</aspect-ratio>
	               <crop>16:9</crop>
	               <has-timeshift>true</has-timeshift>
	               <access>pending</access>
	               <pending-till>1399367372</pending-till>
	               <allowed-till>1401959372</allowed-till>
	            </inetra:stream-inf>
	        </extension>
	        <extension application="http://www.videolan.org/vlc/playlist/0">
	            <vlc:id>0</vlc:id>
	        </extension>
	    </track>
	    <track>
	        <location>udp://@239.1.15.2:1234</location>
	        <title>Россия 1</title>
	        <extension application="http://www.inetra.ru">
	            <inetra:channel-inf>
	               <channel-id>10338258</channel-id>
	               <recordable>false</recordable>
	            </inetra:channel-inf>
	            <inetra:stream-inf>
	               <resolution>720x576</resolution>
	               <access>denied</access>
	            </inetra:stream-inf>
	        </extension>
	        <extension application="http://www.videolan.org/vlc/playlist/0">
	            <vlc:id>1</vlc:id>
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

# Изменения по версиям

## Изменения в версии 2.0.0 (TVREC-70, TVREC-175)

- Начальная редакция.

## Изменения в версии 2.1.0

- Добавлены расширенные атрибуты доступности каналов во времени `pending-till` и `allowed-till` (TVREC-270).

## Изменения в версии 2.1.1

- Добавлен атрибут группировки каналов, реализованный в VLC;
- Добавлены атрибуты возрастного ограничения канала, изменения пропорций и кадрирования изображения (TVREC-276).

## Изменения в версии 3.0.0

- Атрибуты доступности перенесены в характеристики источника вещания;
- Атрибут `allowed` объявлен устаревшим.

## Изменения в версии 3.1.0

- Описание атрибутов `access`, `allowed-till` и `pending-till` вынесены в общий документ.

## Изменения в версии 3.2.0 (TVREC-284)

- Описан атрибут `has-timeshift`;
- Раздел «Атрибуты каналов» заменен ссылкой на раздел «Список каналов» из документа iptv.md.

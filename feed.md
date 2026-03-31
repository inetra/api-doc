title: Feed
quotes language: french
version: 1.0.0
status:  согласован

# Общая информация

Сервис Feed API используется для получения клиентами информации о главном экране продукта (приложения), о наполнении экрана лентами и подборками.

Формат вывода: JSON.

Для обращения за информацией клиент должен быть авторизован, т.е. должен передаваться в запрос валидный токен одним из следующих способов:
- HTTP заголовок **Authorization** (рекомендуемый способ);
- GET параметр запроса **access_token** либо **token**

Подробности в документации по Auth API.

Методы Feed API: *screen*, *feed* и *compilation*.

## Получение экрана продукта определенного типа [screen]

*/feed/1/screen.json*

Ответ содержит  достаточно данных для отображения экрана приложения с первой лентой. Первая лента заполнена полностью, остальные ленты пустые содержат только их идентификаторы и названия, для их наполнения используется метод **feed**

Параметры:

Параметр     | Формат   | По умолчанию | Смысл
-------------|----------|--------------|-------------
`product`    | `строка` | отсутствует  | идентификатор продукта из справочника "Продукты", не чувствителен к регистру
`type`       | `строка` | отсутствует, обязателен |идентификатор типа экрана из справочника "Типы экранов", не чувствителен к регистру type=telecast - получение экрана для телепередачи (!!! смотри описание ниже !!!) 
`telecast`   | `число`  | отсутствует  | идентификатор выпуска телепередачи, используется в комбинации с type=telecast ( !!! смотрите описание ниже !!!)

Пример:
*/feed/1/screen.json?product=ptv&type=home*

Возвращаемое значение

В случае если экран обнаружен, возвращается объект типа Screen:

Экран

	Screen: {
  		title: string,
  		feeds: array of Feed // список лент экрана
	}

Лента

	Feed: {
  		id: string,
  		title: string,
  		compilations: array of Compilation 
	}

Подборка

	Compilation: {   
  		id: string,   
  		title: string,   
  		items: array of Item,  // массив с элементами подборки 
  		itemTypes: array of integer // список всех типов элементов подборки
	}

items -  ограничена по длине, а именно: 15 элементов. Для того чтобы получить оставшиеся элементы (либо постранично) надо использовать метод **compilation**

Item - может содержать разный набор полей, в зависимости от типа подборки

Пример:

	{
		"title": "Главная (Peers.tv)",
  		"feeds": [
    		{
      			"id": "f/9",
      			"title": "Главное",
      			"compilations": [
        			{
          				"id": "c/214484852",
          				"title": "Тема дня",
          				"items": [
            				{
              					"id": 217632168,
              					"title": "Лукашенко: \"Я немного пересидел, но не уйду\"",
              					"rec_id": 217108728,
              					"type": 7,
              					"startTime": 1599582273,
              					"endTime": 1599582352,
              					"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/09/08/217632/217632172.jpg"
            				}
          				],
          				"itemTypes": [7]
        			}
      			]
    		},
    		{
      			"id": "f/10",
      			"title": "Детям"
    		},
    		{
      			"id": "f/12",
      			"title": "Новости"
    		}
  		]
	}

**Подборка записей телепередач**

type = 3, в этом случае объект Item описывает запись телепередачи:

	Item: {
    	id: int not null, // id записи
    	title: varchar not null,
    	type: int not null, // MediaGuideType по документации АПИ Каталога
    	startTime: timestamp not null, // дата и время начала
    	endTime: timestamp not null, // дата и время окончания
    	image: varchar // путь к превью-картинке передачи
	}	

Пример:

	{
		"id": 217530601,
  		"title": "Народный проект. Алтай",
  		"type": 3,
  		"startTime": 1599596700,
  		"endTime": 1599597600,
  		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2019/04/26/159484/159484508.jpg"
	}

**Подборка каналов**

type = 1, в этом случае объект Item описывает канал:

	Item: {
    	id: int not null, // id канала
    	title: varchar not null, // название
    	type: int not null, // MediaGuideType по документации АПИ Каталога
    	image: varchar // путь к лого канала
	}

Пример:

	{
  		"id": 10338245,
  		"title": "Первый",
  		"type": 1,
  		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2015/10/08/55753/55753431.png"
	}

**Подборка нарезок эфира (хайлайтов)**

type = 7, в этом случае объект Item описывает хайлайт (вырезку из записи телепередач):

	Item: {
    	id: int not null, // id хайлайта
    	title: varchar not null,
    	rec_id: int not null, // id записи телепередачи
    	type: int not null, // MediaGuideType по документации АПИ Каталога
    	startTime: timestamp not null,
    	endTime: timestamp not null,
    	image: varchar, // путь к иллюстрации хайлайта
	}

Пример:

	{
  		"id": 217040832,
  		"title": "\"Лихач\". Финал сезона",
  		"rec_id": 216935728,
  		"type": 7,
  		"startTime": 1599175595,
  		"endTime": 1599175640,
  		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/09/04/217040/217040847.jpg"
	}

**Подборки фильмов, сериалов, шоу**

type = 4, 5, 6 соответственно

	Item: {
    	id: int not null, // id афиши
    	type: int not null, // MediaGuideType по документации АПИ Каталога
    	provider: int not null, // id провайдера vod-контента
    	title: varchar not null, // название
    	image: varchar not null, // путь к картинке афиши
    	year: int // год выпуска
	}

Пример:

	{
  		"id": 171105165,
  		"type": 4,
  		"provider": 1,
  		"title": "Прогулка среди могил",
  		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2019/09/13/170857/170857721.jpg",
  		"year": 2014
	}

## Получение содержимого ленты по ее идентификатору [feed]

*/feed/1/feed.json*

Параметры:

Параметр     | Формат   | По умолчанию | Смысл
-------------|----------|--------------|-------------
`id`         |`строка`  |обязателен	   |идентификатор ленты из массива feeds объекта Screen

Пример:

/feed/1/feed.json?id=f/10

Возвращаемое значение

	Feed: {
  		id: string,
  		title: string,
  		compilations: array of Compilation
	}

Как уже говорилось выше, compilations - массив подборок, каждая из которых (items) ограничена по длинне.

Пример:

	{
  		"id": "f/10",
  		"title": "Детям",
  		"compilations": [
    	  {
      		"id": "c/47466347",
      		"title": "Детское ТВ",
      		"items": [
        		{
          			"id": 217323739,
          			"title": "Крошка Милтон",
          			"type": 3,
          			"startTime": 1599598080,
          			"endTime": 1599598380,
          			"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/05/23/205400/205400035.jpg"
        		}
      		],
      		"itemTypes": [3]
    	  }
  		]
	}

## Получение содержимого подборки по ее идентификатору [compilation]

*/feed/1/compilation.json*

Параметры:

Параметр     | Формат   | По умолчанию | Смысл
-------------|----------|--------------|-------------
`id`         |`строка`  |обязателен	   |идентификатор подборки
`limit`      |`число`   |15            |количество элементов в выборке
`offset`     |`число`   |0             |смещение от начала выборки

Примеры запросов:
* /feed/1/compilation.json?id=c/47466347&limit=5&offset=4
* /feed/1/compilation.json?id=c/47466347
* /feed/1/compilation.json?id=c/ch_archive/217323739

Ответ:

	Compilation:  {
  		id: string,
  		title: string,
  		items: array of Item,
  		itemTypes: array of integer
	}

Пример ответа:

	{
  		"id": "c/47466347",
  		"title": "Детское ТВ",
  		"items": [
    	{
      		"id": 217373934,
      		"title": "Песочная анимация киностудии \"Богослов\"",
      		"type": 3,
      		"startTime": 1599596700,
      		"endTime": 1599597300,
      		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2018/07/13/135375/135375410.jpg"
    	},
    	{
      		"id": 217118081,
      		"title": "Это совсем не про это",
      		"type": 3,
      		"startTime": 1599596580,
      		"endTime": 1599596760,
      		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/06/19/208431/208431253.jpg"
    	},
    	{
      		"id": 217070632,
      		"title": "Фильм, фильм, фильм",
      		"type": 3,
      		"startTime": 1599596400,
      		"endTime": 1599597540,
      		"image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/08/28/216327/216327402.jpg"
    	},	
  		],
  		"itemTypes": [3]
	}

## Получение содержимого экрана записи телепередачи

При указании комбинации параметров "type=telecast&telecast=<ID передачи>" генерируется ответ со структурой, которая отличается от описанной выше.

Сделано так чтобы не сломать старые клиенты, где кроме экрана передачи ничего не было.

Формат ответа:

	{
  		title: string,
  		feeds: array of Feed
	}

Пример ответа:

	{
  	"title": "Экран передачи",
  	"feeds": [
    {
      "id": "f/telecast/217323739",
      "title": "Лента передачи",
      "compilations": [
        {
          "id": "c/ch_archive/217323739",
          "title": "Новинки на канале",
          "items": [
            {
              "id": 217323761,
              "type": 3,
              "title": "Джеронимо Стилтон (Geronimo Stilton)",
              "startTime": 1599616140,
              "endTime": 1599617520,
              "image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/05/09/203698/203698484.jpg"
            },
            {
              "id": 217323760,
              "type": 3,
              "title": "Мультимания Караоке",
              "startTime": 1599615420,
              "endTime": 1599616140,
              "image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2019/12/20/183789/183789161.png"
            },
          ],
          "itemTypes": [3]
        },
        {
          "id": "c/ch_popular/217323739",
          "title": "Популярное на канале",
          "items": [
            {
              "id": 217323731,
              "type": 3,
              "title": "Приключения Жюля Верна (JV: The Extraordinary Adventures of Jules Verne)",
              "startTime": 1599589680,
              "endTime": 1599591180,
              "image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2020/05/09/203698/203698477.jpg",
              "views": 91
            },
            {
              "id": 217323721,
              "type": 3,
              "title": "Дрейкерс (Drakers) 17-я серия - \"Просчет Готана\"",
              "startTime": 1599581280,
              "endTime": 1599582960,
              "image": "http://max.1.ptv.bender.inetra.ru/data/illustrations/ills/2019/12/20/183789/183789720.jpg",
              "views": 79
            },
          ],
          "itemTypes": [3]
        }
      ]
    }]
	}

## Нишевый контент

При передачи в заголовке Client-Capabilities знчения niche бекенд передает подборки с типом контента "Нишевый контент"
Пример:
                {
                    "id": "c/common/405623037?product=ptv",
                    "title": "Нишевый контент",
                    "items": [
                        {
                            "id": 405623041,
                            "type": 4,
                            "title": "Гарри Поттер и философский камень.",
                            "image": "http://medinakalmyk.ptv.bender.inetra.ru/data/illustrations/ills/2024/03/22/405623/405623047.jpg",
                            "year": 2001
                        },
                        {
                            "id": 405623035,
                            "type": 4,
                            "title": "Красавица и чудовище",
                            "image": "http://medinakalmyk.ptv.bender.inetra.ru/data/illustrations/ills/2024/03/22/405623/405623046.jpg",
                            "year": 2017
                        }
                    ],
                    "itemTypes": [
                        4
                    ]
                },

## RutubeWeb

При передачи в заголовке Client-Capabilities знчения rutubeweb бекенд в ответе вернет контент с типом поставщика RutubeWeb			


# Изменения по версиям

## Изменения в версии 1.0.0 (PTVRND-1372)

- Начальная редакция документа.

## Изменения в версии 1.1.1 (PTVRND-2220)

- Добавлена поддержка нишевого контента

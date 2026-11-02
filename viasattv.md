---
title: ViasatTV API
quotes language: french
version: 1.0.1
status:  согласован
---

# Общая информация

Сервис ViasatTV API предоставляет доступ к следующей информации:

- список ТВ-каналов, предоставляемых компании Инетра со стороны Viasat
- получение ссылки на поток вещания конкретного канала по его ID

Формат вывода: JSON.

Для обращения за информацией клиент должен быть авторизован.

Документация на "ViPPlay Partner API": https://api-partner.vipplay.ru/

## Список ТВ-каналов <a id="channels.json"></a>

Запрос списка телеканалов, доступных для Партнера ООО "Инетра".

*/viasattv/1/channels.json

Формат ответа:

	message JSONmsg {
 		required double count = 0
  		message ITEMS {
    		required string id = 0
    		required string title = 1
    		required string logo_url = 2
  		}
  		repeated ITEMS items = 1
	}

Пример ответа:

  {
  count: 2,
  items: [
  {
  id: "9d19242c-2093-4065-a28b-5775374ffcc6",
  title: "Viasat Nature/History HD",
  logo_url: "https://viasat-small.cdnvideo.ru/viasat/production/uploads/store/dictionaries/channels/logos/06c6d7b002bcfeac90cdb3f2b228998c.png"
  },
  {
  id: "2bc61cd8-0427-465e-9d4f-fa557c9e398b",
  title: "Viasat Explore",
  logo_url: "https://viasat-small.cdnvideo.ru/viasat/production/uploads/store/dictionaries/channels/logos/7bd382920ec07215f2157dc773179b61.png"
  }
  ]
  }

Где

- count - количество каналов
- items - список каналов

Информация о канале:

- id - идентификатор
- title - название
- logo_url - ссылка на логотип канала

## Получение источника вещания канала <a id="stream.url"></a>

Запроса адаптивного стрима телеканала для партнерского пользователя.

! У пользователя должна быть подписка на контент viasat !

*/viasattv/1/stream.url?channel_id=ID

Параметр:

- channel_id - ID канала из списка channels.json

Формат ответа: пееренаправление (302 код ответа) по адресу вещания потока. Если произойдет какая-то ошибка, то код ответа будет другой, соответствующий ошибке.

"http://api.peers.tv/viasattv/1/stream.url?channel_id=3c43c6e4-7f72-490d-aa4e-393258533850"
можно публиковать в админке сервиса Peers.TV в качестве источников для транскодеров и все будет работать.

# Изменения по версиям

## Изменения в версии 1.0.0 (PTVRND-1576)

- Начальная редакция документа.

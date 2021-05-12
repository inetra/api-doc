title: Purchases
quotes language: french
version: 1.0.0
status:  согласован

# Общая информация

Сервис ViasatTV API предоставляет доступ к следующей информации:
- список ТВ-каналов, предоставляемых компании Инетра со стороны Viasat
- получение ссылки на поток вещания конкретного канала по его ID

Формат вывода: JSON.

Для обращения за информацией клиент НЕ должен быть авторизован, т.е. токен не требуется.

Документация на "ViPPlay Partner API": https://api-partner.vipplay.ru/

## Список ТВ-каналов [channels.json]

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



## Получение источника вещания канала [stream.url]

Запроса адаптивного стрима телеканала для партнерского пользователя.

*/viasattv/1/stream.url?channel_id=<ID>

Параметр:
- channel_id - ID канала из списка channels.json

Формат ответа: пееренаправление (302 код ответа) по адресу вещания потока. Если произойдет какая-то ошибка, то код ответа будет другой, соответствующий ошибке.

Для получения потока каналы был создан специальный служебный пользователь с такими параметрами:

user_email=dumy@mail.ru
user_phone=+79123456987
user_password=password

{
    "encrypted_email": "${encrypted_email}",
    "encrypted_phone": "${encrypted_phone}",
    "password": "${encrypted_password}",
    "sub": {
    "title": "Example sub",
    "duration": 12,
    "duration_unit": "month",
    "start_at": ${current_dt},
        "price": 100,
        "is_trial": false
    }
}

То есть ссылку типа 
"http://api.peers.tv/viasattv/1/stream.url?channel_id=3c43c6e4-7f72-490d-aa4e-393258533850"
можно публиковать в админке сервиса Peers.TV в качестве источников для транскодеров и все будет работать.


# Изменения по версиям

## Изменения в версии 1.0.0 (PTVRND-1576)

- Начальная редакция документа.

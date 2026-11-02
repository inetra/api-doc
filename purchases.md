---
title: Purchases
quotes language: french
version: 1.0.0
status:  согласован
---

# Общая информация

Сервис Purchases API предоставляет доступ к следующей информации:
- список активных покупок
- список приобретенных каналов

Формат вывода: JSON.

Для обращения за информацией клиент должен быть авторизован, т.е. должен передаваться в запрос валидный токен одним из следующих способов:
- HTTP заголовок **Authorization** (рекомендуемый способ);
- GET параметр запроса **access_token** либо **token**

Подробности в документации по Auth API.

## Список активных покупок <a id="list"></a>

*/purchases/1/list.json*

Формат ответа:

	message JSONmsg {
 		required double count = 0
  		message ITEMS {
    		required double id = 0
    		required double user_id = 1
    		required bool is_trial = 2
    		required string product_id = 3
    		required string expires_date = 4
    		required string original_purchase_date = 5
    		required double package_id = 6
    		repeated string package_products = 7
  		}
  		repeated ITEMS items = 1
	}

Пример ответа:

	{
		"count": 1,
		"items": [
			{
				"id": 74036,
				"user_id": 157161,
				"is_trial": false,
				"product_id": "promo_peerstv_plus",
				"expires_date": "2028-11-21 00:00:00+07",
				"original_purchase_date": "2019-05-21 15:15:11+07",
				"package_id": 2,
				"package_products": [
					"ru.inetra.peerstv.plus",
					"ru.inetra.peerstv.plus.discount_29",
					"month_disable_ads",
					"forkids_plus_gp",
					"month_disable_ads_discount29",
					"peers_tv_plus_test",
					"peerstv.ads.disable.site",
					"promo_peerstv_plus",
					"disable_ads_tv",
					"huawei_disable_ads"
				]
			}
		]
	}

Где
- count - количество покупок
- items - список покупок

Информация о покупке:
- id - идентификатор покупки
- user_id - пользователь, совершивший покупку
- is_trial - пробный период есть или нет (true/false)
- product_id - идентификатор купленного продукта
- expires_date - дата истечения срок действия покупки
- original_purchase_date - дата продажи
- package_id - идентификатор купленного пакета
- package_products - список продуктов, куда входит пакет с этим package_id

## Список приобретенных каналов

*/purchases/1/channels.json*

Формат ответа:

	message JSONmsg {
  		required double count = 0
  		repeated float items = 1
	}

Пример ответа:

	{
		"count": 5,
		"items": [
			24970480,
			26552424,
			38248897,
			121141690,
			121802978
		]
	}

Где
- count - количество каналов
- items - список идентификаторов каналов

# Изменения по версиям

## Изменения в версии 1.0.0 (PTVRND-1372)

- Начальная редакция документа.

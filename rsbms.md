title: Recording, Storaging & Balancing Management System API
status: черновик
version: 1.0
jira-ticket: TVREC-380

# Введение

Роли серверов:

- Кодировщик
- Хранилище
- Балансировщик

Общая схема работы:

1. Сервер сообщает свои:
	- идентификатор
	- мощность
	- текущую нагрузку
2. В ответ получает список ролей, которые ему необходимо выполнять и конфигурацию для каждой роли.

Допускается проталкивание конфигураций.

## Описание самочувствия сервера

Чем определяются мощность и нагрузка на сервер?

1. Процессор: измеряется BogoMIPS.
2. Оперативная память измеряется в байтах.
3. Хранилища:
	1. Размер в байтах.
	2. Скорость записи, байт/секунду.
	3. Скорость чтения, байт/секунду.
4. Сетевая подсистема: 
	1. Входящая полоса, бит/секунду.
	2. Исходящая полоса, бит/секунду.

	message Feeling {
		optional string id = 1;
		optional Power power = 2;
		optional Power load_avg = 3;
	}
	
	message Power {
		repeated CPUPower cpus = 1;
		optional int64 ram = 2;
		repeated StoragePower storages = 3;
		repeated NetworkPower networks = 4;
	}
	
	message CPUPower {
		optional int32 order_num = 1;
		optional int32 bogomips = 2;
	}
	
	message StoragePower {
		optional string mount_point = 1;
		optional int64 size = 2;
		optional int64 read_speed = 3;
		optional int64 write_speed = 4;
	}
	
	message NetworkPower {
		optional string iface = 1;
		optional int64 upload_speed = 2;
		optional int64 download_speed = 3;
	}

## Передача списка источников вещания каналов

	message Size {
		optional int32 width = 1;
		optional int32 height = 2;
	}
	
	message Offset {
		optional int32 x = 1;
		optional int32 y = 2;
	}
	
	message Crop {
		optional Offset offset = 1;
		optional Size size = 2;
	}
	
	message StreamSource {
		optional string url = 1;
		optional Crop crop = 2;
		optional Size size = 3;
		repeated string audio_streams = 4;
		
		repeated int64 destination_territories_ids; // ???
	}
	
	message Channel {
		optional int64 channel_id = 1;
	}
	
	message SourcedChannel {
		optional Channel channel = 1;
		repeated StreamSource sources = 2;
	}
	
	message ChannelSources {
		repeated SourcedChannel sourced_channels = 1;
	}

Почему бы список источников не передать m3u8 файлом, как другим клиентам?

## Описание конфигурации Кодировщика

	message KeyValue {
		optional string key = 1;
		optional string value = 2;
	}
	
	message Profile {
		optional int64 profile_id = 1;
		repeated KeyValue options = 2;
	}
	
	message EncodedChannel {
		optional Channel channel = 1;
		optional int64 profile_id = 2;
	}
	
	message CoderTasks {
		repeated EncodedChannel tasks = 1;
	}

## Описание конфигурации Хранилища

	message TimeBounds {
		optional int64 start_time = 1; // может быть не указано
		optional int64 duration = 2;
	}
	
	message StorageTask {
		optional EncodedChannel channel = 1;
		repeated TimeBounds storage_time = 2;
		optional bool fast_access = 3; // поместить в быстрое хранилище, например, оперативную память
		repeated string upstream_coders_ids = 4;
	}
	
	message StorageTasks {
		repeated StorageTask tasks = 1;
	}

## Описание конфигурации балансировщика

	message BalancerTask {
		optional StorageTask storage_task = 1;
		optional string upstream_storages_ids = 2;
	}
	
	message BalancerTasks {
		repeated BalancerTask tasks = 1;
	}

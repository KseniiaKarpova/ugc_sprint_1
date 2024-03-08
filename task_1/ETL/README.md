# Cервис для преобразование данных их Kafka в Clickhouseс ипользованием Airflow


### Руководство по установке и настройке Apache Airflow на сервер с использованием Docker


```Bash
mkdir -p ./logs ./plugins ./config
```

```Bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

```Bash
docker-compose up -d
```

```Bash
docker-compose ps
```
_____________________
go to http://localhost:8080/

Логин: airflow

Пароль: airflow
_____________________


####  Объеденим контайнеры в одну сеть:
```Bash
docker network connect etl_etl-network task_1-kafka-0-1
docker network connect etl_etl-network clickhouse-node1

docker network inspect etl_etl-network
```
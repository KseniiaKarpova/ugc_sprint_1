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

go to http://localhost:8080/

Логин: airflow

Пароль: airflow
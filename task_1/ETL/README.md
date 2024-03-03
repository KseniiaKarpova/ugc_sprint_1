# Cервис для преобразование данных их Kafka в Clickhouseс ипользованием Airflow


### Руководство по установке и настройке Apache Airflow на сервер с использованием Docker

```Bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
```

```Bash
mkdir -p ./dags ./logs ./plugins ./config
```

```Bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
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
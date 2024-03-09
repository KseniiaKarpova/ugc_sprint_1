# Сервис для сохранения данных в Kafka (UGC)
(swager: http://localhost:2090/api/openapi)

# Запуск проекта
### 1 step
create **.env** file based on **.env.example**<br>
```bash
cp env_example .env
```
Edit .env file.
### 2 step
Сборка проекта
```bash
docker-compose up -d --build
```
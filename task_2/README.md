# Исследование: выбор хранилища. `ClickHouse vs Vertica`

Подробные результаты представлены в `ClickHouse vs Vertica.ipynb` 
### Результаты:
Загрузка данных в Vertica пачками в среднем на 1.256 сек занимает большевремени. 
Чтение данных скриптом 
`SELECT * FROM test where some_data=i and gender =g` разница по времени не сильно отличается, но селекст
`SELECT * FROM test where user_id=id` Vertica в среднем занимает в 3 раза больше времени.
### Итог:  
**Выбираем ClickHouse.**

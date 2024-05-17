# Запуск
docker-compose up -d --build

# Просмотр
localhost:8080

Если localhost выдаёт ошибку 500 необходимо проверить загрузку порта командой в терминале: netstat -ano | findstr :8080 (в случае работы в windows) или sudo lsof -i :8080 (в случае wsl). При наличии сторонних процессов в 4u IPv4 закрыть их (taskkill /PID .... /F в win или sudo kill в wsl)

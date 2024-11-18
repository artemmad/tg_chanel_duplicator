#docker build . -t madartem/telegramresender:latest
docker buildx build --platform linux/amd64 -t madartem/telegramresender:latest .
docker push madartem/telegramresender:latest
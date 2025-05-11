import os
import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetMessagesRequest
from loguru import logger
import uuid
import sys

from telethon.tl.types import InputPeerChannel, RpcError, PeerChannel, PeerChat, MessageEntityUrl

SESSIONS_DIR = "conf/sessions"
DOWNLOADS_DIR = "downloads"


class MessageDownloader:
    def __init__(self):
        logger.remove()
        logger.add(
            sys.stderr,
            format="<cyan>{time}</cyan> | <lvl>{level}</lvl> - <lvl>{message}</lvl>",
            colorize=True,
            level="DEBUG",
        )

        logger.add(
            os.path.join("logs", "debug.log"),
            format="{time} {level} {message}",
            level="DEBUG",
            rotation="3mb",
            compression="zip",
        )

        self.config = self._get_config()

        if not os.path.exists(SESSIONS_DIR):
            os.mkdir(SESSIONS_DIR)

        if not os.path.exists(DOWNLOADS_DIR):
            os.mkdir(DOWNLOADS_DIR)

        self.client = TelegramClient(
            os.path.join(SESSIONS_DIR, "account_session"),
            self.config["account_api_id"],
            self.config["account_api_hash"],
        )

    def _get_config(self):
        import json
        with open("conf/config.json", "r", encoding="utf-8") as f:
            return json.load(f)

    async def start(self):
        """
        Запуск клиента и авторизация
        """
        await self.client.start(
            phone=self._get_phone,
            code_callback=self._enter_code,
            password=self._enter_password,
        )
        logger.info("Authorization successful")
        return self

    def _get_phone(self):
        return self.config["account_phone"]

    @staticmethod
    def _enter_code():
        return input("Enter the code from the Telegram message: ")

    @staticmethod
    def _enter_password():
        return input("Enter your two-factor authentication password: ")

    async def download_message(self, message_url):
        """
        Загрузка сообщения и вложений по ссылке
        """
        try:
            logger.info(f"Processing message URL: {message_url}")
            message_url = message_url.replace("https://t.me/c/","")
            parts = message_url.split("/")
            chat_id = int(parts[0].replace("c/", ""))
            message_id = int(parts[-1])

            # Получаем данные о чате
            entity = await self.client.get_entity(PeerChannel(chat_id))

            # Получаем сообщение
            message = await self.client.get_messages(entity, ids=message_id)
            if not message:
                logger.error("Message not found.")
                return

            await self._save_message(message)
        except RpcError as e:
            logger.error(f"Telegram API error: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def _save_message(self, message):
        """
        Сохранение текста сообщения с интегрированными ссылками
        """
        message_dir = os.path.join(DOWNLOADS_DIR, f"message_{message.id}")
        os.makedirs(message_dir, exist_ok=True)

        # Базовый текст сообщения
        text_content = message.message or "No text content"

        # Обработка встроенных ссылок
        if message.entities:
            modified_text = ""
            last_offset = 0
            for entity in message.entities:
                if hasattr(entity, "url"):
                    # Ссылка из MessageEntityTextUrl
                    link_text = text_content[entity.offset:entity.offset + entity.length]
                    link_url = entity.url
                    # Добавляем текст до текущей ссылки, саму ссылку и текст после
                    modified_text += text_content[last_offset:entity.offset] + f"{link_text}({link_url})"
                    last_offset = entity.offset + entity.length
                elif isinstance(entity, MessageEntityUrl):
                    # Ссылка из MessageEntityUrl (сам текст является ссылкой)
                    link_text = text_content[entity.offset:entity.offset + entity.length]
                    modified_text += text_content[last_offset:entity.offset] + f"{link_text}"
                    last_offset = entity.offset + entity.length
            # Добавляем остаток текста
            modified_text += text_content[last_offset:]
            text_content = modified_text

        # Сохранение текста
        text_file_path = os.path.join(message_dir, "message.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        logger.info(f"Message text saved to {text_file_path}")

        # Сохранение медиафайлов
        if message.media:
            media_file_path = os.path.join(message_dir, str(uuid.uuid4()))
            media_file_path = await self.client.download_media(message.media, media_file_path)
            logger.info(f"Media saved to {media_file_path}")
        else:
            logger.info("No media to download")


async def main():
    downloader = MessageDownloader()
    await downloader.start()

    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        message_url = sys.argv[1]
        logger.info(f"Using message URL from arguments: {message_url}")
    else:
        # Ввод ссылки на сообщение
        message_url = input("Enter the message link: ")
        
    await downloader.download_message(message_url)

    await downloader.client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
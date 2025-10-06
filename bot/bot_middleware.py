import csv
import os
from aiogram import BaseMiddleware
from aiogram.types import Message


LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)


ALL_MESSAGES_CSV = os.path.join(LOG_DIR, "all_messages.csv")
UNIQUE_USERS_CSV = os.path.join(LOG_DIR, "unique_users.csv")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            username = event.from_user.username or ""
            text = event.text or ""

            file_exists = os.path.isfile(ALL_MESSAGES_CSV)
            with open(ALL_MESSAGES_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["user_id", "username", "command"])
                writer.writerow([user_id, username, text])

            unique_users = set()
            if os.path.isfile(UNIQUE_USERS_CSV):
                with open(UNIQUE_USERS_CSV, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None) 
                    for row in reader:
                        if row:
                            unique_users.add(row[0])

            if str(user_id) not in unique_users:
                file_exists = os.path.isfile(UNIQUE_USERS_CSV)
                with open(UNIQUE_USERS_CSV, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(["user_id", "username"])
                    writer.writerow([user_id, username])

        return await handler(event, data)

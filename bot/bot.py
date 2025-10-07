from os import getenv
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo, FSInputFile
import asyncio
import logging
import json
from colorama import Style, Fore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, sys, time, threading
from bot_middleware import LoggingMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


MEDIA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "media"))       
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data.json"))

bot = Bot(token=getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.update.middleware(LoggingMiddleware())

ADMIN_GROUP_ID = getenv("ADMIN_GROUP_ID")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    DATA = json.load(f)

START_TEXT = DATA[0]["start_text"]
START_BUTTONS = [[InlineKeyboardButton(text=btn["button_name"], callback_data=btn["callback_data"])] 
                 for btn in DATA if not "start_text" in btn and btn["on_callback"] == ["start"]]
START_BUTTONS.append([InlineKeyboardButton(text="💁‍♀️СВЯЖИТЕСЬ С НАМИ💁‍♀️", callback_data="contact")])

@dp.message(Command(commands=["start"]))
async def on_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=START_BUTTONS)
    await message.answer(text=START_TEXT, reply_markup=keyboard)
    

@dp.callback_query(lambda c: c.data == "start")
async def start_callback(cq: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=START_BUTTONS)
    await cq.message.answer(text=START_TEXT, reply_markup=keyboard)


for button in DATA:
    if not "start_text" in button:
        exec(
f'''
@dp.callback_query(lambda c: c.data == "{button["callback_data"]}")
async def handler_{button["callback_data"]}(cq: CallbackQuery):
    chat_id = cq.message.chat.id
    
    child_buttons = []
    for btn in DATA:
        if not "start_text" in btn and "{button["callback_data"]}" in btn.get("on_callback", []):
            child_buttons.append([InlineKeyboardButton(text=btn["button_name"], callback_data=btn["callback_data"])])

    child_buttons.append([InlineKeyboardButton(text="Назад в меню", callback_data="start")])
    child_buttons.append([InlineKeyboardButton(text="💁‍♀️СВЯЖИТЕСЬ С НАМИ💁‍♀️", callback_data="contact")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=child_buttons) if child_buttons else None

    if keyboard:
        await cq.message.answer(text={json.dumps(button["text"], ensure_ascii=False)}, reply_markup=keyboard)
    else:
        await cq.message.answer(text={json.dumps(button["text"], ensure_ascii=False)})

    media_paths = {button["media"]}
    media = []

    for m in media_paths:
        if m.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            media.append(InputMediaPhoto(media=FSInputFile(MEDIA_DIR  +"/"+ m)))
        elif m.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
            media.append(InputMediaVideo(media=FSInputFile(MEDIA_DIR + "/" + m), width=720, height=1280))

    if media:   
        if len(media) > 10:
            for i in range(len(media)):
                await bot.send_media_group(chat_id=chat_id, media=[media[i]])
        else:
            await bot.send_media_group(chat_id=chat_id, media=media)
    
    await cq.answer()
'''
        )

@dp.callback_query(lambda c: c.data == "contact")
async def handler_contact(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Связаться", callback_data=f"contact_admin")],
        [InlineKeyboardButton(text="Назад в меню", callback_data=f"start")]
    ])
    await callback_query.message.answer(text='''Для связи с менеджером нажмите на кнопку "СВЯЗАТЬСЯ"\nЕсли нажали случайно, можете вернуться в Главное меню.''', reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "contact_admin")
async def contact_admin(callback_query: CallbackQuery):
    username = callback_query.message.chat.username

    await callback_query.message.answer("Благодаримм за ваш интерес к сотрудничеству! Ваша заявка была отправлена админу. C вами свяжутся в ближайшее время для обсуждения деталей.") 
    await bot.send_message(ADMIN_GROUP_ID, text=f"Запрос на сотрудничество от: @{username}.")


class ReloadOnChange(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == DATA_FILE:
            print("⚡ data.json изменился, перезапуск бота...")
            python = sys.executable
            os.execl(python, python, *sys.argv)  


def watch_file():
    event_handler = ReloadOnChange()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(DATA_FILE), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=f"{Fore.GREEN}%(asctime)s{Style.RESET_ALL} | {Fore.BLUE}%(levelname)s{Style.RESET_ALL} | {Fore.YELLOW}%(name)s{Style.RESET_ALL} | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")

    t = threading.Thread(target=watch_file, daemon=True)
    t.start()
    asyncio.run(main())

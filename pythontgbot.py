

from pymongo import MongoClient
import requests
import random
import os
import re
from re import IGNORECASE, escape, search
from telegram import Update
from telegram.error import TelegramError
from telegram.error import BadRequest
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, filters as Filters, MessageHandler, CallbackQueryHandler
import telegram.ext as tg
import re
from telegram.ext import Application
import asyncio
from typing import Union, List, Dict, Callable, Generator, Any
import itertools
from collections.abc import Iterable
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

from telegram import Chat, ChatMember, Update, User
from functools import wraps

BOT_TOKEN = os.environ.get("BOT_TOKEN", None) 
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://zewdatabase:ijoXgdmQ0NCyg9DO@zewgame.urb3i.mongodb.net/ontap?retryWrites=true&w=majority") 

USERS_GROUP = 11


application = Application.builder().token(BOT_TOKEN).build()
asyncio.get_event_loop().run_until_complete(application.bot.initialize())
BOT_ID = application.bot.id





async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
   chat = update.effective_chat
   message = update.effective_message
   try:
       if (
           message.text.startswith("!")
           or message.text.startswith("/")
           or message.text.startswith("?")
           or message.text.startswith("@")
           or message.text.startswith("#")
       ):
           return
   except Exception:
       pass
   vickdb = MongoClient(MONGO_URL)
   vick = vickdb["VickDb"]["Vick"]
   if not message.reply_to_message:
       K = []  
       is_chat = vick.find({"chat":chat.id, "word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       if K:
           hey = random.choice(K)
           is_text = vick.find_one({"chat":chat.id, "text": hey})
           Yo = is_text['check']
# send criteria
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       else:
           await message.reply_text(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
       else:
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:                   
       if message.reply_to_message.from_user.id == BOT_ID:                    
           K = []  
           is_chat = vick.find({"chat":chat.id, "word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           if K:
               hey = random.choice(K)
               is_text = vick.find_one({"chat":chat.id, "text": hey})
               Yo = is_text['check']
# mesz check
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           else:
               await message.reply_text(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")
           else:
               await message.reply_sticker(f"{hey}")

       if not message.reply_to_message.from_user.id == BOT_ID:          
           if message.sticker:
               is_chat = vick.find_one({"chat":chat.id, "word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   vick.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = vick.find_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   vick.insert_one({"chat":chat.id, "word": message.reply_to_message.text, "text": message.text, "check": "none"})



USER_HANDLER = MessageHandler(
    Filters.ALL, log_user, block=False
)
application.add_handler(USER_HANDLER, USERS_GROUP)

print("INFO: BOTTING YOUR CLIENT")
application.run_polling()

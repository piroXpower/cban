

from pyrogram import Client , filters
from pymongo import MongoClient
import os

API_ID = "25789345"
API_HASH = "4f928d05aa0ee47986ea7112c04a84f6"
BOT_TOKEN = ""
MONGO_URL = "mongodb+srv://Belly:belly55@atlascluster.ends7zl.mongodb.net/?retryWrites=true&w=majority"



bot = Client(
    "Level" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

#willbe edited

levelname = ["Team Rocket", "Stray God", "Vector", "Hero Association", "Z Warrior", "Black Knight", "Ghoul", "Overlord"]
levelnum = [2,5,15,25,35,50,70,100]



@bot.on_message(
    filters.command("level", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def levelsystem(_, message): 
    leveldb = MongoClient(MONGO_URL)
   
    toggle = leveldb["ToggleDb"]["Toggle"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_level = toggle.find_one({"chat_id": message.chat.id})
    if not is_level:
        toggle.insert_one({"chat_id": message.chat.id})
        await message.reply_text("Level System Enable")
    else:
        toggle.delete_one({"chat_id": message.chat.id})
        await message.reply_text("Level System Disable")


@bot.on_message(
    (filters.document
     | filters.text
     | filters.photo
     | filters.sticker
     | filters.animation
     | filters.video)
    & ~filters.private,
    group=8,
)
async def level(client, message):
    chat = message.chat.id
    user_id = message.from_user.id    

    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
    toggle = leveldb["ToggleDb"]["Toggle"] 

    is_level = toggle.find_one({"chat_id": message.chat.id})
    if is_level:
        xpnum = level.find_one({"level": user_id, "chatid": chat})

        if not message.from_user.is_bot:
            if xpnum is None:
                newxp = {"level": user_id, "chatid": chat, "xp": 10}
                level.insert_one(newxp)   
                    
            else:
                xp = xpnum["xp"] + 10
                level.update_one({"level": user_id, "chatid": chat}, {
                    "$set": {"xp": xp}})
                l = 0
                while True:
                    if xp < ((50*(l**2))+(50*(l))):
                         break
                    l += 1
                xp -= ((50*((l-1)**2))+(50*(l-1)))
                if xp == 0:
                    await message.reply_text(f"🌟 {message.from_user.mention}, You have reached level {l}**, Nothing can stop you on your way!")
    
                    for lv in range(len(levelname)) and range(len(levellink)):
                            if l == levelnum[lv]:            
                                Link = f"{levellink[lv]}"
                                await message.reply_video(video=Link, caption=f"{message.from_user.mention}, You have reached Rank Name **{levelname[lv]}**")
                  

                               
@bot.on_message(
    filters.command("rank", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rank(client, message):
    chat = message.chat.id
    user_id = message.from_user.id    
    
    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
    toggle = leveldb["ToggleDb"]["Toggle"] 

    is_level = toggle.find_one({"chat_id": message.chat.id})
    if is_level:
        xpnum = level.find_one({"level": user_id, "chatid": chat})
        xp = xpnum["xp"]
        l = 0
        r = 0
        while True:
            if xp < ((50*(l**2))+(50*(l))):
                break
            l += 1

        xp -= ((50*((l-1)**2))+(50*(l-1)))
        rank = level.find().sort("xp", -1)
        for k in rank:
            r += 1
            if xpnum["level"] == k["level"]:
                break                     
        await message.reply_text(f"{message.from_user.mention} Level Info:\nLevel: {l}\nProgess: {xp}/{int(200 *((1/2) * l))}\n Ranking: {r}")




bot.run()

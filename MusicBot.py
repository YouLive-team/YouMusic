import discord
import os,random,asyncio
from discord.ext import commands, tasks
import mysql.connector
from itertools import cycle

async def mydb():
    #Подключаюсь к БД
    db = mysql.connector.connect(
        host=str(os.environ.get("host")),
        user=str(os.environ.get("user")),
        password=str(os.environ.get("password")),
        port="3306",
        database=str(os.environ.get("datebase")),
    )
    return db
    
    
async def custom_prefix(bot, message):
    db = await mydb()
    cursor = db.cursor()

    cursor.execute(f"SELECT prefix FROM server_{message.guild.id}")

    prefix = cursor.fetchone()

    return str(prefix[0])#Тут я возвращаю то значение которое есть в prefix

bot = commands.Bot(command_prefix=custom_prefix)

#Here you should put youtubeapi
YOUTUBE_API = cycle([str(os.environ.get("YT_API1")),
               str(os.environ.get("YT_API2")),
               str(os.environ.get("YT_API3")),
               str(os.environ.get("YT_API4")),
               str(os.environ.get("YT_API5"))
                    ])
#Here you should put in first nikname from yandex music, second password from yandex music
YANDEX_NIKNAME = str(os.environ.get("YANDEX_NIKNAME"))
YANDEX_PASSWORD = str(os.environ.get("YANDEX_PASSWORD"))
YANDEX_TOKEN = str(os.environ.get("YANDEX_TOKEN"))

#Удаление команд
bot.remove_command('help')


async def langueg(ctx):
    db = await mydb()
    cursor = db.cursor()

    cursor.execute(f"SELECT language FROM server_{ctx.guild.id}")

    language = cursor.fetchone()

    return str(language[0])#Тут я возвращаю то значение которое есть в language


@bot.command()
async def ping(ctx):
    await ctx.send("pong")

#Загружаю коги
@bot.command()
async def load(ctx, extensions):
    bot.load_extensions(f'cogs.{extensions}')#Загрузка дополнений
    await ctx.send('loaded')

#Разгрузка
@bot.command()
async def reload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')#Розгрузка дополнений
    await ctx.send('unloaded')

@bot.command()
async def unload(ctx, extensions):
    bot.unload_extension(f'cogs.{extensions}')#Розгрузка дополнений
    bot.load_extensions(f'cogs.{extensions}')#Загрузка дополнений
    await bot.send('unload')





for filename in os.listdir('./cgs'): # Цикл перебирающий файлы в cogs
    if filename.endswith('.py'): # если файл кончается на .py, то это наш ког
        bot.load_extension(f'cgs.{filename[:-3]}')# загрузка дополнений



bot.run(str(os.environ.get("BOT_TOKEN")))

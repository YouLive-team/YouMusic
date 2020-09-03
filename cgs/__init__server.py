import discord
import MusicBot
from discord.ext import commands
import datetime
import mysql.connector
import os


class init_server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.db = await MusicBot.mydb()
        cursor = self.db.cursor()
        try:
            #Создаю таблицу
            cursor.execute(f"CREATE TABLE server_{guild.id} (name TEXT, icon TEXT, region TEXT, premium TEXT, language TEXT, prefix TEXT, music_queue TEXT)")

            #Ввожу данные
            sql = f"INSERT INTO server_{guild.id} (name, icon, region, premium, language, prefix) VALUES (%s, %s, %s, %s, %s, %s)" 
    
            val = (str(guild.name),
                   str(guild.icon),
                   str(guild.region),
                   "N",
                   'ENG',
                   'm.',)
    
            cursor.execute(sql, val)
            self.db.commit()
        except:
            pass

def setup(bot):
    bot.add_cog(init_server(bot))


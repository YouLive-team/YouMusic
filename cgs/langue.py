import discord
import mysql.connector
import re
import os
import MusicBot
from discord.ext import commands

class langue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(aliases = ["lang"])
    @commands.has_permissions(administrator=True)
    async def set_lang(self, ctx, langue: str=None):
        self.db = await MusicBot.mydb()
        if langue == None:
            await ctx.send("ENG or RUS")
        else:
            if langue == 'ENG' or langue == "RUS":
                #Обновляю очередь
                cursor = self.db.cursor()
                
                sql = f"UPDATE server_{ctx.guild.id} SET language = '{langue}'"
                cursor.execute(sql)
                self.db.commit()
                await ctx.send(f"__**{langue}**__")
            else:
                if await MusicBot.langueg(ctx) == "RUS":
                    await ctx.send(f"Извините но я не знаю такой язык, если вы хотите что б он появился в списке языков напишите об этом создателям меня")
                elif await MusicBot.langueg(ctx) == "ENG":
                    await ctx.send(f"Sorry, but I don’t know such a language, if you want it to appear in the list of languages, write to the creators about it")



    @set_lang.error
    async def set_lang_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            if await MusicBot.langue(ctx) == 'RUS':
                await ctx.send(f'**{ctx.author.mention} у вас не достаточно прав**')
            elif await MusicBot.langue(ctx) == 'ENG':
                await ctx.send(f'**{ctx.author.mention} you do not have enough rights**')

def setup(bot):
    bot.add_cog(langue(bot))

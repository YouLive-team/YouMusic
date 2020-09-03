import discord
import re
import mysql.connector
import os
import MusicBot

from discord.ext import commands

class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    #Команда для замены префикса
    @commands.command(aliases = ["pre"])
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix: str):
        self.db = await MusicBot.mydb()
        if len(prefix) >= 3:
            if await MusicBot.langueg(ctx) == "RUS":
                embed=discord.Embed(title=f"Нельзя делать префикс более 2 символов: `{prefix}`",color=0xff7606)
            elif await MusicBot.langueg(ctx) == "ENG":
                embed=discord.Embed(title=f"You cannot prefix more than 2 characters: `{prefix}`",color=0xff7606)
            await ctx.send(embed=embed)
            return
        #Обновляю очередь
        cursor = self.db.cursor()
        
        sql = f"UPDATE server_{ctx.guild.id} SET prefix = '{prefix}'"
        cursor.execute(sql)
        self.db.commit()

        if await MusicBot.langueg(ctx) == "RUS":
            embed=discord.Embed(title=f"__{ctx.author.name}__ изменил префикс: `{prefix}`",color=0xff7606)
        elif await MusicBot.langueg(ctx) == "ENG":
            embed=discord.Embed(title=f"__{ctx.author.name}__ changed prefix: `{prefix}`",color=0xff7606)
        await ctx.send(embed=embed)

    @set_prefix.error
    async def prefix(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
          if await MusicBot.langueg(ctx) == "RUS":
              await ctx.send(f'**{ctx.author.mention} у вас не достаточно прав**')
          elif await MusicBot.langueg(ctx) == "ENG":
              await ctx.send(f'**{ctx.author.mention} you do not have enough rights**')

def setup(bot):
    bot.add_cog(prefix(bot))

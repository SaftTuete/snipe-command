from discord.ext import commands
from discord.commands import slash_command
import discord



class Snipe(commands.Cog):
    def __init__(self, bot, sniped_messages):
        self.bot = bot
        self.bot.sniped_messages = sniped_messages


    @commands.Cog.listener()
    async def on_message_delete(self, message) :
        self.bot.sniped_messages[message.guild.id] = (
        message.content, message.author, message.channel.name, message.created_at)

    @slash_command()
    async def snipe(self, ctx) :
        try :
            contents, author, channel_name, time = self.bot.sniped_messages[ctx.guild.id]

        except :
            await ctx.respond("Couldn't find a message to snipe!", ephemeral=True)
            return

        embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.respond(embed=embed)


def setup(bot) :
    bot.add_cog(Snipe(bot, sniped_messages={}))

import discord
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #Change loreZ to ur desired bot name or the one you have accessed the token of... though giving credits would be appreciated.........
    @commands.command(aliases=["abt"], help="Displays information about the bot (LoreZ).")
    async def about(self, ctx):
        # Access the shared prefix function via self.bot
        current_prefix = self.bot.get_custom_prefix(self.bot, ctx.message)
        
        embed = discord.Embed(
            title="🤖 About LoreZ",
            description="LoreZ is a custom multi-purpose Discord bot.\n\n"
                        "**Developer:** zenobi07\n"
                        f"**Prefix:** {current_prefix}\n"
                        "**Features:** Moderation, Fun commands",
            color=discord.Color.blurple(),
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
import os
import sys
import discord
from discord.ext import commands

# --- CUSTOM CHECK FUNCTION ---
def is_approved():
    """Custom check to see if the user's ID is in the approved list."""
    def predicate(ctx):
        # Check against the list stored in main.py
        return ctx.author.id in ctx.bot.approved_admin_ids
    return commands.check(predicate)
    
class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Example moderation command
    @commands.command(help="Kicks a member from the server. Requires Kick Members permission.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member == ctx.author:
            return await ctx.send("❌ You can't kick yourself!")
        
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("❌ I cannot kick someone who has a higher or equal role to you.")
        
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ Kicked **{member.display_name}** for: **{reason}**")
        except discord.Forbidden:
            await ctx.send("❌ I don't have the necessary permissions to kick that member.")
    
    # --- Graceful Shutdown Command ---
    @commands.command(help="Shuts down the bot gracefully (Approved Admin only).")
    @is_approved()
    async def shutdown(self, ctx):
        """Gracefully shuts down the bot."""
        await ctx.send("🤖 Shutting down gracefully... Bye!")
        await self.bot.close()

    @commands.command(help="Restarts the bot (Approved Admin only).")
    @is_approved()
    async def restart(self, ctx):
        """Shuts down and immediately restarts the bot process."""
        await ctx.send("♻️ Restarting now...")
        await self.bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)


    # --- Cog Reload Command ---
    @commands.command(help="Reloads a specified cog (Approved Admin only).")
    @is_approved()
    async def reload(self, ctx, cog_name: str):
        """Reloads a specified cog."""
        try:
            full_cog_name = f'cogs.{cog_name}'
            self.bot.reload_extension(full_cog_name)
            await ctx.send(f"✅ Successfully **reloaded** the cog: `{cog_name}`")
        except commands.ExtensionNotFound:
            await ctx.send(f"❌ Error: Cog `{cog_name}` not found. Check the filename.")
        except Exception as e:
            await ctx.send(f"❌ Error reloading cog `{cog_name}`: \n```py\n{type(e).__name__}: {e}\n```")
    
async def setup(bot):
    await bot.add_cog(Mod(bot))
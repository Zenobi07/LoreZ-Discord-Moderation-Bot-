from discord.ext import commands
import discord

# -----------------------------

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Assigns the initial Unauthorized role upon joining."""
        if member.bot:
            return 
        
        # Use self.bot to get the ID from main.py
        unauth_role = member.guild.get_role(self.bot.UNAUTHORIZED_ROLE_ID)
        
        if unauth_role:
            try:
                # Assign the Unauthorised User role
                await member.add_roles(unauth_role, reason="Verification Gate: New Member")
            except discord.Forbidden:
                print(f"ERROR: Bot missing permissions to assign role {unauth_role.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Handles verification logic based on reactions."""
        # Ignore reactions from the bot
        if payload.member is None or payload.member.bot:
            return

        # 1. Check if the reaction is on the specific verification message and channel
        # Use self.bot to get IDs from main.py
        if payload.channel_id != self.bot.VERIFY_CHANNEL_ID:
            return
        if payload.message_id != self.bot.VERIFICATION_MESSAGE_ID: 
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = payload.member
        emoji_name = str(payload.emoji)
        
        # 2. Handle Correct Verification Emoji
        # Use self.bot to get config from main.py
        if emoji_name == self.bot.CORRECT_EMOJI:
            unauth_role = guild.get_role(self.bot.UNAUTHORIZED_ROLE_ID)
            member_role = guild.get_role(self.bot.MEMBER_ROLE_ID)
            
            if unauth_role and member_role:
                try:
                    # Grant Member role and remove Unauthorized role
                    await member.remove_roles(unauth_role, reason="Verification Success")
                    await member.add_roles(member_role, reason="Verification Success")
                except discord.Forbidden:
                    print(f"ERROR: Bot missing permissions to manage roles for {member.name}")

        # 3. Handle Wrong Verification Emoji (Kick)
        # Use self.bot to get config from main.py
        elif emoji_name == self.bot.WRONG_EMOJI:
            try:
                # Kick the user
                await member.kick(reason="Failed verification: Selected incorrect option.")
            except discord.Forbidden:
                print(f"ERROR: Bot missing permissions to kick {member.name}")


async def setup(bot):
    await bot.add_cog(Events(bot))
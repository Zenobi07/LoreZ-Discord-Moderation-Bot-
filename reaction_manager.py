import json
import discord
from discord.ext import commands

# The path to our JSON file
REACTION_ROLES_FILE = "reaction_roles.json"

class ReactionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_roles(self):
        """Helper function to save the current roles dict to the JSON file"""
        with open(REACTION_ROLES_FILE, 'w') as f:
            json.dump(self.bot.REACTION_ROLES, f, indent=4)

    # We use a 'group' to make commands like +reaction add/remove
    @commands.group(help="Manages reaction roles. Requires Manage Roles perm.")
    @commands.has_permissions(manage_roles=True)
    async def reaction(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use `+reaction add` or `+reaction remove`.")

    @reaction.command(name="add", help="Adds a new reaction role.")
    async def add_role(self, ctx, message_id: int, emoji: str, role: discord.Role):
        """Adds a reaction role. Usage: +reaction add <message_id> <emoji> <@role>"""
        
        # 1. Convert message_id to string for JSON key
        message_id_str = str(message_id)

        # 2. Get the config for this message, or create it
        if message_id_str not in self.bot.REACTION_ROLES:
            self.bot.REACTION_ROLES[message_id_str] = {
                "type": "add", # Default to 'add' type
                "channel_id": ctx.channel.id # Store channel ID for convenience
            }

        # 3. Add the new emoji/role pair
        self.bot.REACTION_ROLES[message_id_str][emoji] = role.id
        
        # 4. Save the changes to the JSON file
        self.save_roles()

        # 5. Add the reaction to the message so the user can see it
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.add_reaction(emoji)
        except Exception as e:
            await ctx.send(f"⚠️ Warning: Could not add reaction to message: {e}")

        await ctx.send(f"✅ **Added:** Reacting with {emoji} on message `{message_id}` will now give the `{role.name}` role.")

    @reaction.command(name="remove", help="Removes a reaction role.")
    async def remove_role(self, ctx, message_id: int, emoji: str):
        """Removes a reaction role. Usage: +reaction remove <message_id> <emoji>"""
        
        message_id_str = str(message_id)

        # 1. Check if the message is in our config
        if message_id_str not in self.bot.REACTION_ROLES:
            return await ctx.send(f"❌ Error: No reaction roles found for message `{message_id}`.")

        # 2. Check if the emoji is in that message's config
        if emoji not in self.bot.REACTION_ROLES[message_id_str]:
            return await ctx.send(f"❌ Error: The emoji {emoji} is not set up for message `{message_id}`.")

        # 3. Remove the emoji from the config
        removed_role_id = self.bot.REACTION_ROLES[message_id_str].pop(emoji)
        
        # 4. Save the changes to the JSON file
        self.save_roles()

        # 5. Remove the reaction from the message
        try:
            msg = await self.bot.get_channel(self.bot.REACTION_ROLES[message_id_str]['channel_id']).fetch_message(message_id)
            await msg.remove_reaction(emoji, self.bot.user)
        except Exception as e:
            await ctx.send(f"⚠️ Warning: Could not remove reaction from message: {e}")

        await ctx.send(f"✅ **Removed:** Reacting with {emoji} will no longer give a role (was Role ID: `{removed_role_id}`).")


async def setup(bot):
    await bot.add_cog(ReactionManager(bot))
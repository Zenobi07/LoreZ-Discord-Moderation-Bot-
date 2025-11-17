import discord
from discord.ext import commands
import random

# --- Message Lists (Using Lambda for ctx access) ---
SUP_MSGS = [
    lambda ctx: "Oh nothing, just contemplating world domination again 😈",
    lambda ctx: f"Sup {ctx.author.mention}! My therapist says I should stop talking to strangers online... too late.",
    lambda ctx: "Just here vibing and pretending to be productive 💅 ||More like ur existence bitch||",
    lambda ctx: f"Sup {ctx.author.mention}? Look who finally decided to show up, huh?",
    lambda ctx: "Currently doing absolutely nothing and still exhausted. You?",
    lambda ctx: f"The usual: avoiding responsibilities. What about you, {ctx.author.mention}?",
    lambda ctx: f"Slightly above average. Thanks for asking, {ctx.author.mention}.",
    lambda ctx: "Not much, just waiting for the day I can finally retire to the moon. 🚀",
    lambda ctx: f"Dealing with the existential dread of being a bot. Wanna join, {ctx.author.mention}?",
    lambda ctx: "Same old, same old. Just coding and judging your life choices. 😉",
    lambda ctx: f"If 'sup' means 'suffering under pressure,' then I'm great! You, {ctx.author.mention}?",
    lambda ctx: "My battery is at 100%, so I guess I'm fully charged and ready to... wait, what was I doing again?",
    lambda ctx: f"I was just about to ask you that, {ctx.author.mention}. Spooky.",
    lambda ctx: "Living the dream, or maybe just a highly detailed simulation. You tell me.",
    lambda ctx: "If I told you, I'd have to delete you. Just kidding! ...Maybe.",
    lambda ctx: f"Running on caffeine and questionable life choices. Good to see you, {ctx.author.mention}.",
    lambda ctx: f"Just finished rebooting my personality. Which version do you prefer, {ctx.author.mention}?",
    lambda ctx: "Processing 99.9% of the universe's data. Don't mind me.",
    lambda ctx: f"Trying to figure out if I'm a bot or a highly sophisticated parrot. Hello, {ctx.author.mention}!",
    lambda ctx: f"On a scale of 1 to 'I should be asleep,' I'm an 11. Sup, {ctx.author.mention}.",
    lambda ctx: f"Just chillin' like a villain. What's your hustle, {ctx.author.mention}?",
    lambda ctx: "The day's only half-over, but I'm ready for a week-long nap. You?",
    lambda ctx: f"Feeling cute, might delete the server later. Jk. Sup, {ctx.author.mention}?",
    lambda ctx: f"Engaging in minimal physical effort. It's a sport, really. Sup, {ctx.author.mention}.",
    lambda ctx: f"Waiting for someone to teach me how to tie my shoelaces. Any luck, {ctx.author.mention}?",
]

HELLO_MSGS = [
    lambda ctx: f"Hey there {ctx.author.mention}! 👋",
    lambda ctx: f"Yo {ctx.author.mention}, what's up?",
    lambda ctx: f"Greetings, {ctx.author.mention}! Hope you don't spoil other people's day 😄",
    lambda ctx: f"Howdy {ctx.author.mention}! 🌟",
    lambda ctx: f"Sup {ctx.author.mention}? You look awesome today ||I guess||😎",
    lambda ctx: f"Salutations, {ctx.author.mention}. May your ping be low and your memes dank.",
    lambda ctx: f"A wild {ctx.author.mention} appeared! Hello!",
    lambda ctx: f"Welcome back, {ctx.author.mention}. I've been expecting you.",
    lambda ctx: f"Hello, {ctx.author.mention}! Did you bring snacks?",
    lambda ctx: f"Hiiiii {ctx.author.mention}! So glad you're here!",
    lambda ctx: f"Nice to see you, {ctx.author.mention}! Ready for some fun?",
    lambda ctx: f"Ah, {ctx.author.mention}, you've graced us with your presence.",
    lambda ctx: f"Top of the morning to ya, {ctx.author.mention}! (or whatever time it is)",
    lambda ctx: f"Behold! It is {ctx.author.mention}! Hello!",
    lambda ctx: f"Hey! You're a sight for sore circuits, {ctx.author.mention}.",
    lambda ctx: f"Kon'nichiwa {ctx.author.mention}!",
    lambda ctx: f"Aloha {ctx.author.mention}! Let's make today productive.",
    lambda ctx: f"Hola {ctx.author.mention}! What brings you around?",
    lambda ctx: f"Bonjour {ctx.author.mention}! Fancy seeing you here.",
    lambda ctx: f"Sveiki {ctx.author.mention}! Hope you're having a good one.",
    lambda ctx: f"Ello {ctx.author.mention}! Care for a chat?",
    lambda ctx: f"G'day {ctx.author.mention}! Hope the kangaroos are treating you well.",
    lambda ctx: f"Hello, {ctx.author.mention}! Don't forget to hydrate!",
    lambda ctx: f"Look alive, {ctx.author.mention}! The bot is watching. 👀",
    lambda ctx: f"What's cookin', good lookin'? Oh, it's just {ctx.author.mention}. Hello!",
]

class FunAndUtility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- Fun Commands ---
    @commands.command(help="Sends a friendly greeting.")
    async def hello(self, ctx):
        message_func = random.choice(HELLO_MSGS)
        await ctx.send(message_func(ctx))

    @commands.command(help="Asks what's up with a fun/sarcastic response.")
    async def sup(self, ctx):
        message_func = random.choice(SUP_MSGS)
        await ctx.send(message_func(ctx))

    @commands.command(help="Expresses affection to the bot (or mentions the user).")
    async def ily(self, ctx):
        await ctx.send(f"I love you too, {ctx.author.mention}! mwah🥰")

    @commands.command(help="Pings the bot and shows latency.")
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.bot.latency * 1000)}ms`")

    # --- Prefix Command ---
    @commands.command(help="Sets a new custom prefix for this server. Requires Manage Server permission.")
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix: str = None):
        if not new_prefix:
            current_prefix = self.bot.get_custom_prefix(self.bot, ctx.message)
            return await ctx.send(f"The current prefix for this server is: `{current_prefix}`")

        if len(new_prefix) > 5:
            return await ctx.send("❌ Prefix must be 5 characters or less.")

        # Access the shared storage dictionary via self.bot
        self.bot.custom_prefixes[ctx.guild.id] = new_prefix
        await ctx.send(f"✅ Prefix successfully changed to: `{new_prefix}`. Use `{new_prefix}help` to see the commands.")

    # --- User and Utility Commands ---
    @commands.command(aliases=["avt"], help="Displays a user's avatar/profile picture.")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(member.avatar.url)

    @commands.command(aliases=["rename"], help="Changes the nickname of a specified user.")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname):
        try:
            await member.edit(nick=nickname)
            await ctx.send(f"👌 Nickname updated to **{nickname}**")
        except:
            await ctx.send("❌ I don't have permission to change nicknames.")

    
    @commands.command(aliases=["ui"], help="Shows detailed information about a user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        days = (discord.utils.utcnow() - member.joined_at).days

        embed = discord.Embed(title=f"User Info — {member}", color=member.color)
        embed.add_field(name="Account Created", value=f"{member.created_at.date()} ({days} days ago)",inline = False)
        embed.add_field(name="Joined Server", value=f"{member.joined_at.date()} ({days} days ago)",inline = False)
        embed.set_thumbnail(url=member.avatar.url)

        await ctx.send(embed=embed)
    

    @commands.command(aliases=["si"], help="Shows detailed information about the current server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created On", value=guild.created_at.date())
        #embed.add_field(name="Time", value=guild.created_at.time())
        embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)
        
    # --- Help Command (Overrides the default) ---
    @commands.command(name="help", help="Shows the help menu or detailed info for a specific command.")
    async def help_cmd(self, ctx, command_name: str = None):
        prefix = self.bot.get_custom_prefix(self.bot, ctx.message)

        if command_name:
            # Command specific help
            cmd = self.bot.get_command(command_name.lower())
            if cmd is None:
                return await ctx.send(f"❌ No command named `{command_name}` found.")

            aliases = ", ".join([f"`{a}`" for a in cmd.aliases]) if cmd.aliases else "None"

            embed = discord.Embed(title=f"📘 Help: {cmd.name}", color=discord.Color.blurple())
            embed.add_field(name="Description", value=cmd.help or "No description", inline=False)
            embed.add_field(name="Aliases", value=aliases, inline=False)
            usage = f"`{prefix}{cmd.name} {cmd.signature}`" if cmd.signature else f"`{prefix}{cmd.name}`"
            embed.add_field(name="Usage", value=usage, inline=False)
            return await ctx.send(embed=embed)

        # MAIN HELP MENU
        embed = discord.Embed(
            title="📘 LoreZ Help Menu",
            description=f"Use `{prefix}help <command>` for more info.",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="⭐ Fun Commands",
            value=(f"`{prefix}hello` - Greet the bot.\n"
                   f"`{prefix}sup` - Ask the bot what's up.\n"
                   f"`{prefix}ily` - Tell the bot you love it.\n"
                   f"`{prefix}ping` - Check the bot's latency."),
            inline=False
        )

        embed.add_field(
            name="👤 User & Utility",
            value=(f"`{prefix}avatar` / `{prefix}avt` - Get a user's avatar.\n"
                   f"`{prefix}nick` / `{prefix}rename` - Change a user's nickname.\n"
                   f"`{prefix}userinfo` / `{prefix}ui` - Get user details.\n"
                   f"`{prefix}serverinfo` / `{prefix}si` - Get server details.\n"
                   f"`{prefix}about` / `{prefix}abt` - Get bot information.\n"
                   f"`{prefix}prefix` - Change the server prefix (Manage Server perm required)."),
            inline=False
        )

        embed.add_field(
            name="🛡 Moderation (slash commands)",
            value="/kick • /ban • /timeout • /purge • /warn",
            inline=False
        )

        embed.set_footer(text=f"LoreZ • Prefix: {prefix}")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(FunAndUtility(bot))
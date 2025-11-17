import os
import logging
import json # Import JSON
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# --- JSON FILE CONFIG ---
REACTION_ROLES_FILE = "reaction_roles.json"

def load_reaction_roles():
    """Loads reaction roles from the JSON file."""
    try:
        with open(REACTION_ROLES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("reaction_roles.json not found. Creating a new one.")
        with open(REACTION_ROLES_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    except json.JSONDecodeError:
        print("Error decoding reaction_roles.json! Starting with empty config.")
        return {}

# -----------------------------
# Configuration & Dynamic Prefix Setup
# -----------------------------
CUSTOM_PREFIXES = {}
DEFAULT_PREFIX = "+"

APPROVED_ADMIN_IDS = [
    123456789,  # Replace these numbers with the user id of owner/admins
    123456789,
]

def get_custom_prefix(bot, message):
    """Retrieves the custom prefix for the guild, or the default prefix."""
    if message.guild:
        return CUSTOM_PREFIXES.get(message.guild.id, DEFAULT_PREFIX)
    return DEFAULT_PREFIX

# -----------------------------
# Logging Setup
# -----------------------------
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
discord.utils.setup_logging(handler=handler, root=False, level=logging.INFO)


# -----------------------------
# Bot Initialization & Cog Loading
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  
intents.guilds = True

bot = commands.Bot(
    command_prefix=get_custom_prefix, 
    intents=intents, 
    help_command=None,
    owner_id=APPROVED_ADMIN_IDS[0] # Sets the primary owner ID from line 35
)

# Store shared data on the bot object
bot.custom_prefixes = CUSTOM_PREFIXES
bot.get_custom_prefix = get_custom_prefix
bot.approved_admin_ids = APPROVED_ADMIN_IDS 

# --- REACTION ROLE CONFIG ---
bot.UNAUTHORIZED_ROLE_ID = 123456789 # for the reaction verification of users on join not necessary until you wanna use this feature

# Load roles from JSON file into the bot
bot.REACTION_ROLES = load_reaction_roles()
print(f"Loaded {len(bot.REACTION_ROLES)} reaction role messages from JSON.")

# ------------------------------------------
#read readme for info on these
# --- ADD YOUR VERIFICATION SETUP TO THE JSON MANUALLY ---
# You should add your verification message to the JSON file
# using the new +reaction add command once the bot is running.
# Or, you can add it here as a default *if it's not in the file*.
# Example:
# if "456789012345678901" not in bot.REACTION_ROLES:
#     bot.REACTION_ROLES["456789012345678901"] = {
#         "type": "verify",
#         "remove_role": bot.UNAUTHORIZED_ROLE_ID,
#         "✅": 123456789,
#         "❌": "KICK"
#     }
#     print("Added default verification role to config.")
#     # Save this default back to the file
#     with open(REACTION_ROLES_FILE, 'w') as f:
#         json.dump(bot.REACTION_ROLES, f, indent=4)
# ------------------------------------------


COGS_TO_LOAD = [
    'cogs.events',
    'cogs.fun_and_utility',
    'cogs.mod', 
    'cogs.about',
    'cogs.reaction_manager'  
]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    # Load all cogs dynamically
    for cog in COGS_TO_LOAD:
        try:
            await bot.load_extension(cog) 
            print(f"Loaded extension: {cog}")
        except commands.ExtensionError as e:
            print(f"Failed to load extension {cog}: {e}")
            
# -----------------------------
# RUN BOT
# -----------------------------
bot.run(TOKEN)
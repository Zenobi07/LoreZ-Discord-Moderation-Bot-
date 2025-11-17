LoreZ Discord Bot
A customizable, multi-purpose Discord bot built with discord.py. Features moderation, fun commands, utility functions, and a powerful reaction role system.
Features
● Fun Commands: hello, sup, ily, ping
● Utility Commands: about, avatar, userinfo, serverinfo, prefix
● Moderation: kick, nick (rename)
● Reaction Roles: Fully configurable reaction roles using JSON.
● Admin: shutdown, restart, reload (for bot owner only)
Installation & Setup
Follow these steps to get your own instance of the bot running.
1. Prerequisites
● Python 3.8 or higher
● A Discord Bot Token (from the Discord Developer Portal)
2. Clone & Organize Files
1. Clone this repository to your local machine or server.
2. In the main project folder, create a new directory named cogs.
3. Move all of the following Python files into the cogs directory:
○ about.py
○ events.py
○ fun_and_utility.py
○ mod.py
○ reaction_manager.py
(Your main folder should now contain main.py, .env, reaction_roles.json, and the new cogs folder. If you plan to use a welcome GIF, make sure the GIF file is also placed in this main folder.)
4. Log File: The bot will automatically generate a discord.log file in the main folder. This file is useful for debugging and seeing errors.
3. Install Dependencies
Install the required Python libraries using pip. A requirements.txt file is included for ease.
pip install -r requirements.txt
4. Configure Environment
1. Find the .env file.
2. Open it and add your Discord Bot Token: DISCORD_TOKEN=YourBotTokenGoesHere
5. Configure main.py
1. Open main.py with a code editor.
2. Set Admin IDs: Find the APPROVED_ADMIN_IDS list (around line 34) and replace the placeholder numbers with your own Discord User ID. This gives you access to commands like +shutdown and +reload. APPROVED_ADMIN_IDS = [ 123456789012345678, # Replace with your User ID ]
3. Set Unauthorized Role ID: Find bot.UNAUTHORIZED_ROLE_ID (around line 81) and replace the placeholder with the ID of the "unverified" or "guest" role on your server. This is needed for the verification setup. bot.UNAUTHORIZED_ROLE_ID = 123456789012345678 # ID of your "Unverified" role
4. (Optional but Recommended): The events.py cog contains an older, hardcoded verification system. To avoid conflicts with the new system, it's best to disable it. In main.py (around line 124), find the COGS_TO_LOAD list and remove 'cogs.events'.
6. Run the Bot
Once configured, you can start the bot:
python main.py
How to Use Reaction Roles (Verify & Standard)
Here is your step-by-step plan to get the reaction role system running. Please follow these steps in order.
1. First-Time Setup (One-Time-Only)
This step adds a default "Verify" rule to your reaction_roles.json file.
1. Uncomment the Block: Open main.py. Find the section around line 112 that starts with # --- ADD YOUR VERIFICATION SETUP....
2. Uncomment all 12 lines in that block (remove the # from the start of each line).
3. Run the Bot: Start your bot (python main.py).
You should see this in your console:
Added default verification role to config.
2. Verify the JSON
1. Open your reaction_roles.json file.
2. It should no longer be empty. It should now contain the full setup for your verification message, including the "type": "verify" and "❌": "KICK" parts.
3. "Lock In" Your Changes
1. Stop the bot.
2. Go back to main.py.
3. Re-comment the 12 lines you just uncommented. (Put the # back at the start of each one).
○ This is very important. It prevents the bot from trying to add this default rule every single time it starts.
4. Test The New Commands
Now for the fun part. Start your bot again. It will now load your verification rule from the JSON file.
A. Test +reaction add (for standard roles):
1. Go to a channel.
2. Send a message like "Get your color roles here!"
3. Right-click the message and Copy ID.
4. Create a test role (e.g., @TestRed).
5. In the channel, type the command (using the ID you just copied): +reaction add 1234567890123456789 🔴 @TestRed
6. The bot should reply "✅ Added:..." and automatically add the 🔴 reaction to your message.
B. Test +reaction remove:
1. Now, remove the rule you just made: +reaction remove 1234567890123456789 🔴
2. The bot should reply "✅ Removed:..." and remove its 🔴 reaction from the message.
⚠️
A Quick Warning on Emojis
● Unicode Emojis: Standard emojis (like 🔴, 👍, ✅) will work perfectly.
● Custom Emojis: If you want to use a custom server emoji, use the emoji itself in the command, don't just type its name.
○ Do this: +reaction add 123 <:my_emoji:123> @role
○ Not this: +reaction add 123 :my_emoji: @role (This will fail with an "Unknown Emoji" error).
Commands
The default prefix is +. This can be changed per-server with the +prefix command.
Command
Description
Fun
+hello
Greet the bot.
+sup
Ask the bot what's up.
+ily
Tell the bot you love it.
+ping
Check the bot's latency.
Utility
+about
Displays information about the bot.
+avatar [member]
Displays a user's avatar.
+userinfo [member]
Shows detailed information about a user.
+serverinfo
Shows detailed information about the server.
+prefix [new_prefix]
Sets a new prefix (Requires Manage Server).
+nick <member> <name>
Changes a user's nickname (Requires Manage Nicknames).
Moderation
+kick <member> [reason]
Kicks a member (Requires Kick Members).
Reaction Roles
+reaction add <msg_id> <emoji> <@role>
Adds a new reaction role (Requires Manage Roles).
+reaction remove <msg_id> <emoji>
Removes a reaction role (Requires Manage Roles).
Admin Only
+shutdown
Shuts down the bot gracefully.
+restart
Restarts the bot.
+reload <cog_name>
Reloads a specific cog (e.g., fun_and_utility).
Contact
For any doubts, questions, or contributions, feel free to reach out:
● Discord: zenobi07
● GitHub: https://github.com/Zenobi07

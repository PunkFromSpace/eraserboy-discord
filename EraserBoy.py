import discord
from discord.ext import commands
from datetime import timedelta
import os
import json
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

bot_token = os.getenv('ERASERBOY_TOKEN')
log_server_id = os.getenv('LOGSERVER_ID')
reckless_devil_id = int(os.getenv('RECKLESS_DEVIL_ID'))

# Print the loaded values for debugging
#print(f"Bot Token: {bot_token}")
#print(f"Log Server ID: {log_server_id}")  

# Let EraserBoy read messages
intents = discord.Intents.default()
intents.message_content = True 
intents.guilds = True
intents.presences = True
intents.members = True


# Load server_to_log_channel from JSON
def load_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            return json.load(f)
    return {"server_to_log_channel": {}}

# Save server_to_log_channel to JSON
def save_config(data):
    with open('config.json', 'w') as f:
        json.dump(data, f, indent=4)

# Initialize server_to_log_channel
config = load_config()
server_to_log_channel = config['server_to_log_channel']

# Set command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# For when the bot's online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Restriction to ADMIN
'''
@bot.check
async def global_check_admin(ctx):
    return ctx.author.guild_permissions.administrator
'''

# Restriction to Reckless Check
def is_reckless():
    def predicate(ctx):
        print(f"Checking user ID: {ctx.author.id} against {reckless_devil_id}")  # Debugging output
        return ctx.author.id == reckless_devil_id
    return commands.check(predicate)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Hello, {ctx.author.mention}. Looks like you either spelled something wrong or are trying an invalid command. Try !cmdlist to see the command list.")
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f"Don't be a bad little thing now, {ctx.author.mention}. Only mommy and daddy allowed.")

# A BIT OF SECURITY
channel_creation_lock = asyncio.Lock()

# SERVER ENTRY CHECK
'''
@bot.event
async def on_guild_join(guild):
    log_channel_name = f"log-{guild.name.replace(' ', '-').lower()}"
    log_server = bot.get_guild(log_server_id)

    if log_server is None:
        print("Log server not found. Please check your log_server_id.")
        return

    log_category = discord.utils.get(log_server.categories, id=log_category_id)

    if log_category is None:
        print(f"Log category with ID {log_category_id} not found in the log server.")
        return

    try:
        existing_channel = discord.utils.get(log_category.text_channels, name=log_channel_name)
        if existing_channel:
            server_to_log_channel[guild.id] = existing_channel.id
            print(f"Log channel already exists: {existing_channel.name}")
        else:
            # Attempt to create a new log channel
            new_log_channel = await log_server.create_text_channel(log_channel_name, category=log_category)
            server_to_log_channel[guild.id] = new_log_channel.id
            print(f"Created new log channel: {new_log_channel.name}")

        # Save the updated mapping to JSON
        save_config({"server_to_log_channel": server_to_log_channel})

    except discord.Forbidden:
        print(f"Bot lacks permissions to create a channel in {log_server.name}.")
    except Exception as e:
        print(f"Error creating log channel: {str(e)}")
'''

# ----- COMMANDS DOWN HERE----------

# Help Command
@bot.command()
async def cmdlist(ctx):
    """List all available commands and their descriptions."""
    help_message = "Here are the available commands:\n\n"
    
    for command in bot.commands:
        # Ignore the help command to avoid recursion
        if command.name != 'cmdlist':
            help_message += f"!{command.name}: {command.help}\n"
    
    await ctx.send(help_message)

# Test Command
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def hello(ctx):
    """Tests if the bot is online. And a nice little greeting."""
    await ctx.send(f'Hello, {ctx.author.mention}! EraserBoy is ONLINE.')

# Test Command - For Reckless
@bot.command()
@is_reckless()
async def hi(ctx):
    """Tests if the bot is online, but ONLY for RecklessDevil."""
    await ctx.send(f'Heyyyy, {ctx.author.mention}! EraserBoy is ONLINE. How are you, sweetheart?')

@hi.error
async def hi_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("No no, that's for Reckless Devil only. Try \'!hello\' instead")

# Bad Boy
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def badboy(ctx):
    """For when the bot's been a bad little shit."""
    await ctx.send(f'I\'m so sorry. I deserve punishment. Please punish me. I need it to become a good little thing. I\'m so sorry, master. I deserve this.')

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def spankbadboy(ctx):
    """To punish the bad boy"""
    await ctx.send("OWA! OWA! OWA OWA OWA! YES, I DESERVE THIS! OWA! I'M SORRY!")

# Good Boy
@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def goodboy(ctx):
    """For undeserved praise."""
    await ctx.send(f"Thank you :3\nI don't deserve that kinda recognition but it's nice hehehehe")

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.has_permissions(administrator = True)
async def headpatgoodboy(ctx):
    """For undeserved reward."""
    await ctx.send(f"HEHEHEHEHEHE THANK U <3")

# You Bad Little Thing
@bot.command()
async def badlittlething(ctx, member: discord.Member, *, reason=None ):
    """To call out your fellow server members on their bad behavior. Can't be caught with your hand in the cookie jar and NOT get in trouble now, can you?"""
    if member is None:
        await ctx.send(f"Hello, {ctx.author.mention}. Please mention a member to call out for their behavior.")
    if reason is None:
        await ctx.send(f'You\'ve been such a bad little thing, {member.mention}. Truly such a horrid little stain on this server. Be better. Do better. Fix yourself. Get some help.')
    else:
        await ctx.send(f'Wowwww, {member.mention}. {ctx.author.mention} says you\'ve been a horrid little thing. You... {reason}?? That\'s not great. Do better. Be better.')   

# Purge Command
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
@commands.has_permissions(administrator = True)
async def purge(ctx, amount: int):
    """Purges any specified number of messages."""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} previous messages deleted by {ctx.author.mention}!')
'''
# Ghost Purge Command
@commands.cooldown(1, 60, commands.BucketType.user)  # Cooldown to prevent DoS attacks
@bot.command()
@commands.has_permissions(manage_messages=True)
async def ghostpurge(ctx, amount: int):
    """Purges a specified number of messages and logs them in a designated channel for each server."""
    
    # Purge messages and keep a list of deleted messages
    deleted_messages = await ctx.channel.purge(limit=amount + 1)

    # Check if there is a log channel mapped for the current server (guild)
    log_channel_id = server_to_log_channel.get(ctx.guild.id)

    # If no log channel exists yet for this server, create one
    if log_channel_id is None:
        async with channel_creation_lock:  # Ensure only one log channel is created at a time
            # Double-check if the channel exists to avoid race conditions
            log_channel_id = server_to_log_channel.get(ctx.guild.id)
            if log_channel_id is None:
                # Get the log channel name and your personal server
                log_channel_name = f"log-{ctx.guild.name.replace(' ', '-').lower()}"
                log_server = bot.get_guild(log_server_id)

                # Get the specific category in which to create the log channels
                log_category = discord.utils.get(log_server.categories, id=log_category_id)

                # Try to create the log channel and handle potential errors
                try:
                    # Check if the log channel already exists in the category
                    existing_channel = discord.utils.get(log_category.text_channels, name=log_channel_name)
                    if existing_channel:
                        log_channel_id = existing_channel.id
                    else:
                        # Create a new log channel in the specified category
                        new_log_channel = await log_server.create_text_channel(log_channel_name, category=log_category)
                        log_channel_id = new_log_channel.id

                    # Store the mapping in memory
                    server_to_log_channel[ctx.guild.id] = log_channel_id

                except discord.Forbidden:
                    await ctx.send(f"Bot lacks permissions to create the log channel in {log_server.name}.")
                    return
                except Exception as e:
                    await ctx.send(f"An error occurred while creating the log channel: {str(e)}")
                    return

    # Log details in the mapped log channel
    log_channel = bot.get_channel(log_channel_id)

    if log_channel is None:
        print(f"Log channel is missing for {ctx.guild.name}. Creating a new one.")
    # You can add your code here to recreate the log channel if needed, or just log this for further action.
        return

    # Prepare the initial log message
    log_message = f'**{ctx.author}** purged **{len(deleted_messages)}** messages in **#{ctx.channel}** (Server: **{ctx.guild.name}**).\n\n'
    log_message += '**Deleted Messages:**\n'

    for msg in deleted_messages:
        # Add the author and timestamp
        log_message += f'- {msg.author} at {msg.created_at}: '

        # Handling message content
        if msg.content:
            # Check if the message exceeds 2000 characters
            if len(msg.content) > 2000:
                log_message += f'(Message too long, truncated)\n{msg.content[:1997]}...\n'
            else:
                log_message += f'{msg.content}\n'
        else:
            log_message += '(No message content)\n'

        # Handling attachments
        if msg.attachments:
            for attachment in msg.attachments:
                log_message += f'   [Attachment]: {attachment.url}\n'

        # Check if the log message itself is about to exceed the Discord message limit
        if len(log_message) > 1900:
            # Send partial log and start a new message
            try:
                await log_channel.send(log_message)
            except discord.HTTPException as e:
                await ctx.send(f"An error occurred while sending log messages: {str(e)}")
            log_message = ''  # Clear log message buffer after sending

    # Send any remaining log message if it's not empty
    if log_message:
        try:
            await log_channel.send(log_message)
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred while sending log messages: {str(e)}")

# Error handler for cooldown
@ghostpurge.error
async def ghostpurge_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Try again in {int(error.retry_after)} seconds.")
'''

# Kick Command
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kick a member from the server."""
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick this member.")
    except discord.HTTPException:
        await ctx.send("Failed to kick the member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Ban Command
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban a member from the server."""
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban this member.")
    except discord.HTTPException:
        await ctx.send("Failed to ban the member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Timeout Command (also called mute in some contexts)
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: str, *, reason=None):
    """Timeout a member for a specified duration."""
    time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}  # Seconds in each unit
    if duration[-1] in time_units:
        unit = duration[-1]
        try:
            value = int(duration[:-1])
            seconds = value * time_units[unit]

            if seconds > 0 and seconds <= 31536000:  # Limit to 1 year
                await member.timeout(seconds=seconds, reason=reason)
                await ctx.send(f'Timed out {member.mention} for {value} {unit}.')
            else:
                await ctx.send("Duration must be between 1 second and 1 year.")
        except ValueError:
            await ctx.send("Invalid duration format. Use formats like '1m', '12s', '3h', '2d', 'y'.")
    else:
        await ctx.send("Invalid duration unit. Use 's', 'm', 'h', 'd', or 'y'.")

# Remove Timeout Command (Unmute)
@bot.command()
@commands.has_permissions(moderate_members=True)
async def remove_timeout(ctx, member: discord.Member):
    """Remove the timeout from a member."""
    try:
        await member.timeout(None)  # Remove timeout by setting it to None
        await ctx.send(f'Removed timeout from {member.mention}.')
    except discord.Forbidden:
        await ctx.send("I don't have permission to remove the timeout for this member.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


# Invite a User Command
@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
@commands.has_permissions(create_instant_invite=True)
async def invite(ctx, user_id: int):
    """Create an invite link and send it to a user by their ID, mentioning the inviter."""
    try:
        user = await bot.fetch_user(user_id)  # Fetch the user object
        print(f"Fetched user: {user}")  # Debugging line

        invite = await ctx.guild.create_invite(max_age=86400)  # Create a temporary invite link (valid for 1 day)
        print(f"Invite created: {invite}")  # Debugging line

        # Send invite with mention
        await user.send(f"You've been invited to join the server by {ctx.author.mention}! Here’s your invite link: {invite}")
        await ctx.send(f"Invite link sent to {user.name}#{user.discriminator}.")
    except discord.NotFound:
        await ctx.send("The specified user ID does not exist.")
        print("User not found.")
    except discord.Forbidden:
        await ctx.send("Bot cannot send DMs to this user. Make sure their DMs are open.")
        print("Cannot send DMs to the user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        print(f"Error: {str(e)}")  # Debugging line

@bot.command()
@commands.is_owner()
async def check_online(ctx, member: discord.Member = None):
    """Check member online status."""
    if member:
        # Check the status of the specified member
        if member.status == discord.Status.offline:
            await ctx.send(f"{member.display_name} appears to be offline or invisible.")
        else:
            await ctx.send(f"{member.display_name} is currently online with status: {member.status}.")
    else:
        # Separate active users and bots
        online_users = [m.display_name for m in ctx.guild.members if m.status != discord.Status.offline and not m.bot]
        online_bots = [m.display_name for m in ctx.guild.members if m.status != discord.Status.offline and m.bot]
        
        # Count of online users and bots
        total_users = len(online_users)
        total_bots = len(online_bots)
        
        # Create the response message
        response = f"**Total Online Members:** {total_users + total_bots}\n"
        response += f"**Active Users:** {total_users}\n**Active Bots:** {total_bots}\n\n"
        
        # Add online members and bots lists
        if online_users:
            response += "Active Users:\n" + "\n".join(online_users)
        else:
            response += "No active users are currently online."

        response += "\n\n"

        if online_bots:
            response += "Active Bots:\n" + "\n".join(online_bots)
        else:
            response += "No bots are currently online."

        await ctx.send(response)


# Run the bot with your token
bot.run(bot_token)

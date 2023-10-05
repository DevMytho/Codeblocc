import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from discord import file
from easy_pil import Editor, load_image_async, Font


bot = commands.Bot(command_prefix='#', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    listen = discord.Game("/𝐡𝐞𝐥𝐩")
    await bot.change_presence(status=discord.Status.dnd, activity=listen)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.remove_command('help')


@bot.tree.command(name="hello", description=" Says hello to the user who used it ")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello !! {interaction.user.mention} :wave_tone1: ")


@bot.tree.command(name="ping", description="Says the ping of the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"`{round(bot.latency * 1000)}ms!!`")


@bot.tree.command(name="clear", description="Clears/Purges all the messages")
@app_commands.describe(amount="The number of messages to clear")
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.send_message("Clearing messages :thumbsup_tone1:")
    await interaction.channel.purge(limit=amount + 1)


@bot.tree.command(name="kick", description="Kicks the member")
@app_commands.describe(reason="The reason to kick")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"Kicked {member.name} from {member.guild.name} for reason: " + reason)
    await member.kick(reason=reason)


@bot.tree.command(name="ban", description="Bans the member from the server")
@app_commands.describe(reason="The reason to ban")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str):
    await interaction.response.send_message(f"Banned {member.name} from {member.guild.name} for reason: " + reason)
    await member.ban(reason=reason)

@bot.tree.command(name="broadcast", description="Creates a Random Embbed Broadcast Message")
async def broadcast(interaction: discord.Interaction, text:str):
    embed = discord.Embed(title = text , color = discord.Color.random())
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="help", description="Prints list of all commands of the bot")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the commands of the Codeblocc :blush: :tada:"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/emojis/852564308864008222.gif?size=48")

    embed.add_field(
        name="help", value="This prints the help page", inline=True)
    embed.add_field(name="ping", value="This gives ping of Neve", inline=True)
    embed.add_field(name="broadcast", value="Random Broadcasted Emmbed Message", inline=True)
    embed.add_field(
        name="hello", value="Says hello to the user who used the command", inline=True)
    embed.add_field(
        name="clear", value="Purges the required number of messages", inline=True)
    embed.add_field(
        name="kick", value="Kicks the selected member from the server", inline=True)
    embed.add_field(
        name="ban", value="Bans the selected member from the server", inline=True)
    await interaction.response.send_message(embed=embed)


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel

    background = Editor("bg.gif")
    profile_image = await load_image_async(str(member.avatar.url))

    profile = Editor(profile_image).resize((250, 250)).circle_image()
    poppins = Font.poppins(size=75, variant="bold")

    poppins_small = Font.poppins(size=65, variant="light")

    background.paste(profile, (550, 200))
    background.ellipse((550, 200), 250, 250, outline="Black", stroke_width=3)

    background.text(
        (700, 450), f"Welcome To {member.guild.name}", color="Black", font=poppins, align="center")
    background.text((700, 555), f"{member.name}#{member.discriminator}",
                    color="Black", font=poppins_small, align="center")

    file = discord.File(fp=background.image_bytes, filename="bg.gif")
    await channel.send(f"{member.mention}! **Welcome To {member.guild.name} Please Read Rules**")
    await channel.send(file=file)

bot.run("MTE1OTUxODEyNjc4NzAyMjk2MA.GvIyOR.FEMKwmm-IEKPlDX56_HgJ0RqEaXOCfGOGYyBfE")

# Import lib yang dibutuhkan
from groq import Groq
from dotenv import load_dotenv
import os
from typing import Final
import discord
from discord.ext import commands

# Load Macam Token
load_dotenv()
TOKEN_BOT: Final[str] = os.getenv('BOT_TOKEN')
TOKEN_GROQ: Final[str] = os.getenv('AI_KEY')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Inisialisasi bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
ai_groq = Groq(api_key=TOKEN_GROQ)

# Event dan command buat bot Tams
@bot.event
async def on_ready():
    print(f'{bot.user} Siap digunakan')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello! Saya Tams dan tuan saya adalah Arya Wiratama, Asisten Pribadi Kamu!, Ada yang bisa saya bantu?')

@bot.command()
async def goodbye(ctx):
    await ctx.send("Goodbye! Sampai Jumpa Lagi!")

# Groq Respon AI
@bot.command()
async def tanya(ctx, *, pertanyaan):
    try:
        chat_ai = ai_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Jawab pertanyaan ini dalam bahasa indonesia : {pertanyaan}"""
                }
            ], 
            model="llama-3.3-70b-versatile",
            stream=False
        )
        ai_output = chat_ai.choices[0].message.content
        await ctx.send(ai_output)
    except:
        await ctx.send("Maaf, saya tidak mengerti")


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Hello {member.name}, Selamat Datang Di Server!")

@bot.event
async def on_member_remove(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"{member.name} Telah meninggalkan Server!")

bot.run(TOKEN_BOT)
import discord
import os
from config import disord_token, gemini_token, guild_ids
from google import genai
from google.genai import types

client = genai.Client(api_key=gemini_token)

bot = discord.Bot()

image_names = os.listdir("images")
system_instruction = "주어지는 메시지에 대해 각각 적절한 대답을 주어진 반응 중에서 골라. 대답은 오직 반응 숫자 하나로.\n"    
for i, name in enumerate(image_names):
    system_instruction += f"{i}. {name}\n"

def kim_react_image(contents):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        )
    )
    index = int(response.text)
    image_name = image_names[index]
    return image_name

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=guild_ids)
async def kim_talk(ctx, message):
    image_name = kim_react_image(message)
    file = discord.File(f"images/{image_name}")
    await ctx.respond(f"'{message}'", file=file)

@bot.message_command(name="(대충김경일짤)", guild_ids=guild_ids)
async def kim_jjal(ctx, message: discord.Message):
    image_name= kim_react_image(message.content)
    file = discord.File(f"images/{image_name}")
    await ctx.respond(file=file)

bot.run(disord_token)
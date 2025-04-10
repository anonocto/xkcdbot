import discord
import feedparser
import asyncio
import os

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = YOUR_CHANNEL_ID  # Replace with your channel ID
RSS_URL = "https://xkcd.com/atom.xml"  # XKCD Atom feed

intents = discord.Intents.default()
client = discord.Client(intents=intents)

latest_post = None

async def fetch_latest_comic():
    global latest_post
    feed = feedparser.parse(RSS_URL)
    if feed.entries:
        entry = feed.entries[0]
        title = entry.title
        link = entry.link
        img_url = entry.media_content[0]['url'] if 'media_content' in entry else None
        return title, link, img_url
    return None, None, None

async def check_rss():
    global latest_post
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    while not client.is_closed():
        title, link, img_url = await fetch_latest_comic()
        if title and link and latest_post != link:
            latest_post = link
            embed = discord.Embed(title=title, url=link, color=0x00ff00)
            if img_url:
                embed.set_image(url=img_url)
            await channel.send(embed=embed)
        await asyncio.sleep(3600)  # Check every hour

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(check_rss())

client.run(TOKEN)

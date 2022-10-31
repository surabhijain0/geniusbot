"""Discord bot that provides artist, album, and song information from Genius"""
import logging
import os
import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GENIUS = 'https://genius.com/'

bot = commands.Bot(command_prefix='.', intents=discord.Intents.default())
bot.intents.message_content = True

discord.utils.setup_logging(level=logging.DEBUG, root=False)

@bot.event
async def on_ready():
    """Prints log in message to console"""
    print(f'We have logged in as {bot.user}')

@bot.command()
async def artist(ctx, arg_field, arg_artist):
    """Sends artist information"""
    url = GENIUS + 'artists/' + arg_artist

    if arg_field == 'albums':
        class_attr = 'thumbnail_grid'
        sep = '\n'
    elif arg_field == 'songs':
        class_attr = 'mini_card_grid'
        sep = ' '
    else:
        await ctx.send('Invalid info parameter')
        return

    texts = scrape_info(url, class_attr, sep)
    for text in texts:
        if arg_field == 'albums' and text != texts[0] and text != texts[1]:
            text = text[:len(text) - 5]
        if arg_field == 'songs' and text != texts[0]:
            text = text[:text.index(artist - 1)]
        if not (arg_field == 'albums' and text == texts[1]):
            await ctx.send(text)

    return

@bot.command()
async def album(ctx, arg_field, arg_artist, arg_album):
    """Sends album information"""
    url = GENIUS + 'albums/' + arg_artist + '/' + arg_album
    sep = ' '

    if arg_field == 'credits':
        class_attr = 'metadata_unit'
    elif arg_field == 'tracklist':
        class_attr = 'chart_row-content'
    else:
        await ctx.send('Invalid info parameter')
        return

    texts = scrape_info(url, class_attr, sep)
    for text in texts:
        if arg_field == 'tracklist' and text != texts[0] and text != texts[1]:
            text = text[:text.index(' Lyrics')]
        await ctx.send(text)

    return

@bot.command()
async def song(ctx, arg_field, arg_artist, arg_song):
    """Sends song information"""
    url = GENIUS + arg_artist + '-' + arg_song + '-lyrics'
    sep = ' '

    if arg_field == 'credits':
        class_attr = 'SongInfo__Credit'
    elif arg_field == 'about':
        class_attr = 'ExpandableContent__Content'
    elif arg_field == 'lyrics':
        class_attr = 'Lyrics__Container'
        sep = '\n'
    else:
        await ctx.send('Invalid info parameter')
        return

    texts = scrape_info(url, class_attr, sep)
    for text in texts:
        if text.find('Sample') >= 0 or text.find('Interpol') >= 0:
            break
        await ctx.send(text)

    return

def scrape_info(url, class_attr, sep):
    """Returns array of text content given url, tag, and formatting parameters"""
    url = url.replace(' ', '-')
    webpage = requests.get(url, timeout=1)

    if not webpage.ok:
        return ['Invalid artist, album, or song']

    texts = []
    html = BeautifulSoup(webpage.content, 'html.parser')
    title = html.find('title').texts
    titles = title[:title.index(' Lyrics')].split(' – ')
    for title in titles:
        texts += title.split(' - ')
    for tag in html.select(f'div[class^="{class_attr}"]'):
        for i in tag.select('i'):
            i.unwrap()
        tag.smooth()
        text = tag.get_texts(strip=True, separator=sep)
        if text:
            texts.append(text)
    return texts

bot.run(TOKEN)

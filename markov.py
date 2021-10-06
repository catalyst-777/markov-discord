"""A Markov chain generator that can tweet random messages."""

import sys
from random import choice
import discord
import os

def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ''
    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()
    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    keys = list(chains.keys())
    key = choice(keys)

    words = [key[0], key[1]]
    while key in chains:


        word = choice(chains[key])
        words.append(word)
        key = (key[1], word)

    return ' '.join(words)


token = os.getenv("Discord_Token")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    filenames = sys.argv[1:]
    text = open_and_read_file(filenames)
    chains = make_chains(text)
    msg = make_text(chains)

    await message.channel.send(msg)

client.run(token)



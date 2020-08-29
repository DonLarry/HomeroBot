"""
    @author DonLarry
    @bot HomeroBot
    @version 1.1
    @brief This is a Discord bot for the Discord Channel of Galindo Team
"""

import discord
import math
import datetime
from datetime import timezone
from settings import BOT_TOKEN, GENERAL_CHANNEL, BID_CHANNEL, LOG_CHANNEL


out = {
    'GENERAL': None,
    'BID': None,
    'LOG': None
}


client = discord.Client()
bid_lifetime = 86400
bids = []


async def log(message):
    print(out['LOG'])
    await out['LOG'].send(message)


@client.event
async def on_ready():
    global out
    out['GENERAL'] = client.get_channel(GENERAL_CHANNEL)
    out['BID'] = client.get_channel(BID_CHANNEL)
    out['LOG'] = client.get_channel(LOG_CHANNEL)
    await out['GENERAL'].send("Hello Galindo Teen!")
    await out['GENERAL'].send(file=discord.File('homer-1.jpg'))
    await out['GENERAL'].send("Excuse me, Galindo Team*")
    await out['GENERAL'].send(file=discord.File('homer-2.jpg'))
    await log('ONREADY -> OPEN')
    ########################################################
    to_delete = []
    now = datetime.datetime.now(timezone.utc)
    now = now.replace(tzinfo=None)
    deletions = 0
    async for message in out['BID'].history():
        dt = message.created_at
        dif = (now-dt).total_seconds()
        if dif > bid_lifetime:
            try:
                await message.delete()
            except Exception as e:
                log(f'Exception deleting message.\ne : {e}')
            else:
                deletions += 1
            continue
        wait = bid_lifetime - dif
        to_delete.append([message,wait])
    await log(f'\tDeletions at start: {deletions}')
    await log(f'\tRemainding bids: {len(to_delete)}')
    ########################################################
    await log('TO_DELETE')
    for message, t in to_delete:
        await message.delete(delay=t)
        await log('Deleted bid')
    await log('ONREADY -> CLOSE')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    #debugging
    #print(message)
    content = message.content.split()
    channel = client.get_channel(message.channel.id)
    if len(content)>0:
        if content[0] == "!delete_logs":
            if len(content) != 2:
                await channel.send('Invalid format.\nExpected: !delete_logs <int>')
                return
            else:
                logs = int(content[1])
                if math.isnan(logs):
                    channel.send('expected "!delete_logs <int>"')
                elif message.author.id == 668439228430155816:
                    try:
                        await out['LOG'].purge(limit=logs)
                    except Exception as e:
                        channel.send(f'Exception: {e}')
                else:
                    channel.send(f'{message.author.name} tried to do some command')

    if message.channel.id == BID_CHANNEL:
        await message.delete(delay=bid_lifetime)
    if message.channel.id == LOG_CHANNEL:
        await message.delete()


@client.event
async def on_member_join(member):
    await out['GENERAL'].send(f"Welcome {str(member).split('#')[0]}!")


if __name__ == "__main__":
    client.run(BOT_TOKEN)

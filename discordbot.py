from distutils.sysconfig import PREFIX
import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import os

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']
CHANNEL_ID = 1063880677436690552
MAX_SESSION_TIME_MINUTES = 1
PC_COUNT = 2
pcStatusList = []
isSentList = []
timeList = []
timeTemp = datetime.now().strftime("%H%M%S")
now = int(str(timeTemp)[0:2])*3600 + int(str(timeTemp)[2:4])*60 + int(str(timeTemp)[4:6])
for i in range(PC_COUNT):
    pcStatusList.append(0)
    isSentList.append(0)
    timeList.append(now)

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Hello, Checking bot is ready!')
    channel = client.get_channel(CHANNEL_ID)
    client.loop.create_task(watch())
    await channel.send("Hello, Checking bot is ready!")

async def watch():
    pcNumber = 1
    channel = client.get_channel(CHANNEL_ID)

    while True:
        bound = MAX_SESSION_TIME_MINUTES * 10
        intTime = bound
        while intTime > 2:
            async for message in channel.history(limit=1):
                timeTemp = datetime.now().strftime("%H%M%S")
                now = int(str(timeTemp)[0:2]) * 3600 + int(str(timeTemp)[2:4]) * 60 + int(str(timeTemp)[4:6])
                # curDate = int(str(message.created_at.time())[0:2]) * 3600 + \
                #           int(str(message.created_at.time())[3:5]) * 60 + int(str(message.created_at.time())[6:8])
                if message.content.endswith('is working'):
                    pcNumber = int(message.content.replace('is working', '').replace('pc', '').strip())
                    if pcStatusList[pcNumber] == 0:
                        pcStatusList[pcNumber] = 1
                        timeList[pcNumber] = now
                        isSentList[pcNumber] = 0
                    else:
                        pcStatusList[pcNumber] = 2
                        timeList[pcNumber] = now
                        isSentList[pcNumber] = 0
                    # await message.delete()
                    await channel.purge(limit=1)

            await asyncio.sleep(1)
            intTime -= 1

        order = 0
        timeTemp = datetime.now().strftime("%H%M%S")
        now = int(str(timeTemp)[0:2]) * 3600 + int(str(timeTemp)[2:4]) * 60 + int(str(timeTemp)[4:6])
        for pastTime in timeList:
            if (int(now - pastTime)) > bound:
                if pcStatusList[order] == 0:
                    if isSentList[order] == 0:
                        isSentList[order] = 0
                    else:
                        isSentList[order] = 1
                else:
                    isSentList[order] = 0
                pcStatusList[order] = 0
                timeList[order] = now

            order += 1

        order = 0
        for pcStatus in pcStatusList:
            if pcStatus == 0 and isSentList[order] == 0:
                isSentList[order] = 1
                print("computer" + str(order) + " Was Stopped")
            if pcStatus == 1 and isSentList[order] == 0:
                isSentList[order] = 1
                print("computer" + str(order) + " Was Started")
            if pcStatus == 2:
                isSentList[order] = 0
            order += 1

def is_me(m):
    return m.author == client.user

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")

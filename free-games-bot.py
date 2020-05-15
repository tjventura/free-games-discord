import discord, time, random, json 
import epic_games_parser.parser as parser

messages = ['WOW some free games available my dudes!', 
    'I am currently working but here are the free games that i could find.',
    'A computer? A machine? I am a bot! and i have games for you!',
    'My boss is a completly jerk, i have to do all the work around here. Here are some free games.',
    'Hello its me, boterino, grab your free games!']

epicGames = ['','','','','','']

with open('epicGamesCache.txt') as fp:
    lines = fp.readlines()

i = 0
for line in lines:
    epicGames[i] = line.strip() + '\n'
    i+=1
i = 0

f = open("token.txt", "r")
token = f.read()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await sendEmbedMessage(client)

def embedMessage(games):
    gameTitle = games['title']
    startDate = games['startDate'].replace('T', '  ')[:-5]
    endDate = games['endDate'].replace('T', '  ')[:-5]
    thumbnail = games['thumbnail']

    embedMessage = discord.Embed(title = gameTitle,  colour=discord.colour.Color.blurple())
    embedMessage.add_field(name="Starts at: ", value=startDate)
    embedMessage.add_field(name="Ends at: ", value=endDate)
    embedMessage.add_field(name="Grab them at: ", value='www.epicgames.com', inline=False)
    embedMessage.set_thumbnail(url=thumbnail)
    return embedMessage


async def timer(client):
    time.sleep(10)
    print('30 secs have passed')
    await sendEmbedMessage(client)

async def sendEmbedMessage(client):
    gamesInfo = json.loads(parser.fetcher())
    i = 0
    DBChanged = False
    for games in gamesInfo:
        if epicGames[i] != (games['title'] + '\n'):
            DBChanged = True
            epicGames[i] = games['title'] + '\n'
            if i == 0:
                await client.get_channel(710855974633734165).send(random.choice(messages))
            await client.get_channel(710855974633734165).send(embed=embedMessage(games))
        i+=1
    i = 0

    if DBChanged:
        writeDB()

    time.sleep(3600)

    await timer(client)

def writeDB():
    with open("epicGamesCache.txt", "w") as db:
        db.writelines(epicGames)

client = MyClient()
client.run(token)
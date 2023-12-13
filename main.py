#pip install discord
import discord
import datetime
import asyncio
import requests

#Declare variable so it isn't null
input = ""


#Discord bot settings
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents,activity=discord.Game(name='Escape from Tarkov'))


#Define API request
def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

async def ping(message,msgSplit, pingCounter):
    myChannel = client.get_channel(846123908683661322)
    nameList = []
    x=1
    for x in range(msgSplit.length):
        if msgSplit[x] == "<" or msgSplit[x]==">":
            break
        else:
            nameList.append(msgSplit[x])
    input =" ".join(nameList)
    if pingCounter > 48:
        await myChannel.send(f'The ping limit has been reached for "{input}", the ping limit is 48 hours')
        pingCounter = 0
        return
    new_query = f"""
    {{
        items(name: "{input}") {{
            name
            sellFor {{
                price
                source
            }}
        }}
    }}
    """
    result = run_query(new_query)
    response = str(result)
    responseSplit =response.split()
    reversedList = []
    for x in responseSplit:
        reversedList = [x] + reversedList

    if msgSplit[nameList.length + 1] == "<":
        if reversedList[2] < int(msgSplit[nameList.length + 2]):
            botResponse = str("<@" + str(message.author) + ">" + "The price on the Flea market for "+ input +" is now "+ (reversedList[2]))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(3600)
            await ping(message,msgSplit, pingCounter)
    elif msgSplit[nameList.length + 1] == ">":
        if reversedList[2] > int(msgSplit[nameList.length + 2]):
            botResponse = str("<@" + str(message.author) + ">" + "The price on the Flea market for "+ input +" is now "+ (reversedList[2]))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(3600)
            await ping(message,msgSplit, pingCounter)
    else:
        await message.channel.send("Invalid input please use this format: Ping *item name* < or > *price* for example: Ping Metal Fuel < 1000")



async def handleMsg(message,msgSplit):
    input =" ".join(msgSplit[1:])
    new_query = f"""
    {{
        items(name: "{input}") {{
            name
            sellFor {{
                price
                source
            }}
        }}
    }}
    """
    result = run_query(new_query)
    #Spaghetticode begins. Only god and i knew what this code meant when i wrote it, now only god knows
    response = str(result)
    responseSplit =response.split()
    reversedList = []
    nameList = []
    for x in responseSplit:
        reversedList = [x] + reversedList
    #Tries gathering real name not typed input
    if responseSplit[2] =="[{'name':":
        #Still gathers even if the name is multiple words 
        x=3
        for x in range(3,10):
            if responseSplit[x]=="'sellFor':":
                break
            else:
                nameList.append(responseSplit[x])
        #Sends message to discord with the real name
        if reversedList[0] =="'fleaMarket'}]}]}}":
            botResponse = str("The price on the Flea market for "+ " ".join(nameList) +" is "+ (reversedList[2]))
            await message.channel.send(botResponse)
        else:
            await message.channel.send("That item is not on the Flea Market or a skill issue ocurred")
    else:
        #Sends message to discord with the input name
        if reversedList[0] =="'fleaMarket'}]}]}}":
            botResponse = str("The price on the Flea market for "+ input +" is "+ (reversedList[2]))
            await message.channel.send(botResponse)
        else:
            await message.channel.send("That item is not on the Flea Market or a skill issue ocurred")

#On Log in
@client.event
async def on_ready():
    pingCounter = 0
    print('Logged in as {0.user}'.format(client))
    #Bot recieves message
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        msgSplit = message.content.split()
        if msgSplit[0] =="Fleabot":
            await handleMsg(message,msgSplit)
        if msgSplit[0] =="Ping":
            await ping(message,msgSplit, pingCounter)

#Add your discord bot token    
client.run('MTE0NjAwMTI4NTY5MTIzMjI5Ng.G4fRd7.SP126XQH3FkvUCXvphwgexfn3j7_xGAoWsSgtg')
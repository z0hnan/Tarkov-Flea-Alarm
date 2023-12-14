#pip install discord
import discord
import datetime
import asyncio
import requests
import json

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
    myChannel = message.channel
    nameList = []
    for x in range(len(msgSplit)):
        if msgSplit[x] == "<" or msgSplit[x]==">":
            break
        else:
            if msgSplit[x] != "Ping":
                nameList.append(msgSplit[x])
    input =" ".join(nameList)
    if pingCounter > 96:
        await myChannel.send(f'The ping limit has been reached for "{input}", the tracking limit is 48 hours')
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
     
    # Access the JSON response directly without replacing
    items_list = result.get('data', {}).get('items', [])

    # Initialize item_name with None
    item_name = None
    # Initialize flea_market_price with None
    flea_market_price = None

    # Check if the 'items' list is not empty
    if items_list:
        # Take the first item (assuming there's only one)
        data = items_list[0]

        # Extract the item name
        item_name = data.get('name')

        # Extract the price from the source 'fleaMarket'
        flea_market_price = next(
            (item.get('price') for item in data.get('sellFor', []) if item.get('source') == 'fleaMarket'),
            None
        )
    if item_name is not None:
        printName = item_name
    else:
        printName = input

    if msgSplit[len(nameList) + 1] == "<":
        if float(flea_market_price) < float(msgSplit[len(nameList) + 2]):
            botResponse = str("<@" + str(message.author.id) + ">" + " The price on the Flea market for "+ printName +" is now "+ str(flea_market_price))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(1800)
            await ping(message,msgSplit, pingCounter)
    elif msgSplit[len(nameList) + 1] == ">":
        if float(flea_market_price) > float(msgSplit[len(nameList) + 2]):
            botResponse = str("<@" + str(message.author.id) + ">" + " The price on the Flea market for "+ printName +" is now "+ str(flea_market_price))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(1800)
            await ping(message,msgSplit, pingCounter)
    else:
        await message.channel.send("Invalid input please use this format: Ping *item name* < or > *price* for example: Ping Metal Fuel < 1000")



async def handleMsg(message,msgSplit):
    input =" ".join(msgSplit[1:])
    new_query = f"""
{{
    items(name: "{input}"){{
        name
        sellFor{{
            price
            source
        }}
    }}
}}
"""
    result = run_query(new_query)
     
    # Access the JSON response directly without replacing
    items_list = result.get('data', {}).get('items', [])

    # Initialize item_name with None
    item_name = None
    # Initialize flea_market_price with None
    flea_market_price = None

    # Check if the 'items' list is not empty
    if items_list:
        # Take the first item (assuming there's only one)
        data = items_list[0]

        # Extract the item name
        item_name = data.get('name')

        # Extract the price from the source 'fleaMarket'
        flea_market_price = next(
            (item.get('price') for item in data.get('sellFor', []) if item.get('source') == 'fleaMarket'),
            None
        )
    
    #Tests if real name exists
    if item_name is not None:
        printName = item_name
    else:
        printName = input

    #Sends message to discord
    if flea_market_price is not None:
        botResponse = str("The price on the Flea market for "+ printName +" is "+ str(flea_market_price))
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
client.run('MTE0NjAwMTI4NTY5MTIzMjI5Ng.GAodA7.AD2j28bwKzOLjQZX07oexw-xOPZqcPquzw4kXY')

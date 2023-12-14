#pip install discord
import discord
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
    #Tests if real name exists
    if item_name is not None:
        printName = item_name
    else:
        printName = input
    #Sends message to discord if price couldn't be found
    if flea_market_price is None:
        await message.channel.send(f"{input} is not on the Flea Market or a skill issue ocurred. Please use this format: Ping *item name* < or > *price* for example: Ping Metal Fuel < 1000")
        return

    operator = msgSplit[len(msgSplit)-2]   
    targetPrice = msgSplit[len(msgSplit)-1]

    if operator == "<":
        if float(flea_market_price) < float(targetPrice):
            botResponse = str("<@" + str(message.author.id) + ">" + " The price on the Flea market for "+ printName +" is now "+ str(flea_market_price))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(1800)
            await ping(message,msgSplit, pingCounter)
    elif operator == ">":
        if float(flea_market_price) > float(targetPrice):
            botResponse = str("<@" + str(message.author.id) + ">" + " The price on the Flea market for "+ printName +" is now "+ str(flea_market_price))
            await message.channel.send(botResponse)
        else:
            pingCounter = pingCounter + 1
            await asyncio.sleep(1800)
            await ping(message,msgSplit, pingCounter)
    else:
        await message.channel.send("Invalid input please use this format: Ping *item name* < or > *price* for example: Ping Metal Fuel < 1000")


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
        if msgSplit[0].lower() =="fleabot":
            if len(msgSplit)!=1:
                await handleMsg(message,msgSplit)
            else:
                await message.channel.send("Please enter an item name after Fleabot")
        if msgSplit[0].lower() =="ping":
            if len(msgSplit)!=1:
                await ping(message,msgSplit, pingCounter)
            else:
                await message.channel.send("Invalid input please use this format: Ping *item name* < or > *price* for example: Ping Metal Fuel < 1000")
        if msgSplit[0].lower() =="help":
            await message.channel.send("Fleabot is a bot that will ping you when an item reaches a certain price, and it can also tell you the price of an item on demand on the Flea Market. To use it type: \nFleabot *item*\nFor example: Fleabot Metal Fuel \nyou can also use the command \nPing *item name* < or > *price* \nFor example: Ping Metal Fuel < 1000")

#Add your discord bot token    
client.run('---YOUR TOKEN HERE---')

#pip install discord
import discord
import datetime
import asyncio
import requests


input = ""
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents,activity=discord.Game(name='Escape from Tarkov'))


def run_query(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post('https://api.tarkov.dev/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))



    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        msgSplit = message.content.split()

        if msgSplit[0] =="Fleabot":
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
            response = str(result)
            responseSplit =response.split()
            reversedList = []
            for value in responseSplit:
                reversedList = [value] + reversedList

            if reversedList[0] =="'fleaMarket'}]}]}}":
                botResponse = str("The price on the Flea market for "+ input +" is "+ (reversedList[2]))
                await message.channel.send(botResponse)
            else:
                await message.channel.send("That item is not on the Flea Market or a skill issue ocurred")
    
client.run('MTE0NjAwMTI4NTY5MTIzMjI5Ng.G4G44c.ugqWlO1-g-f9eQMHJjHLmcCkv-SivTVbV_LB6Q')
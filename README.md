# Tarkov-Flea-Alarm
A discord bot that pings you when an item reaches a set price, and can check prices on demand

To invite this bot to your discord server, use this invite link:

https://discord.com/api/oauth2/authorize?client_id=1146001285691232296&permissions=2048&scope=bot

To self host this bot you need to create a discord bot and insert its token at the bottom.
You also need a newer version of Python, and finally install the packages that are commented out at the top.
This code is best run on a raspberry pi or other server as it needs to be up constantly

The commands to use the bot is either

Fleabot "*item name*" For example "Fleabot Metal Fuel" for checking prices on demand

or

Ping "*item name*" < or > "*price*" For example "Ping Metal Fuel > 300000" for notifying if an item drops or reaches a certain price within 48 hours(Configurable) 


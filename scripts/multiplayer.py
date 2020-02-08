import applescript
import discord
import pyperclip


asecretkey = ''

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

	if message.content.startswith('$host klk-spex'):
		pass

	if message.content.startswith('$host chickens'):
		print('message author: {0}'.format(message.author))
		await message.channel.send('Creating 2p Lobby...')
		applescript.tell.app("Keyboard Maestro Engine",'do script "9C1EEAC8-DB27-4772-B047-0BBA4751F14A"') # chickens 1
		cb = pyperclip.paste()
		await message.channel.send('Lobby Code: {0}'.format(cb))
		applescript.tell.app("Keyboard Maestro Engine",'do script "D6F7C0CE-9445-4BEC-9134-888A763C4CE2"') # chickens 2
		await message.channel.send('Redeploy?')
		

client.run(asecretkey)


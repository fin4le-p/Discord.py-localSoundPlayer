import discord
import mojimoji
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get('TOKEN')

fastHunt = "."
client = discord.Client()
allSound: int = 220 + 1


@client.event
async def on_ready():

    print("The bot has logged in")
    game = discord.Game("https://sara-hoshikawa.com")
    await client.change_presence(activity=game)


@client.event
async def on_message(message: discord.Message):
    # メッセージの送信者がbotだった場合は無視する

    try:

        if message.author.bot:
            return

        print(message.author.name + '#' + message.author.discriminator + ' : ' + message.content)

        if message.content == fastHunt + "list":
            await message.channel.send("ボイスの一覧、利用規約は下記をご覧ください。\n規約・使い方：https://sara-hoshikawa.com/bot/download\nボイスリスト：https://sara-hoshikawa.com/bot/voicelist")

        elif message.content == fastHunt + "stop":
            if message.guild.voice_client is None:
                await message.channel.send("接続していません。")
                return
            
            message.guild.voice_client.stop()
            return

        elif message.content == fastHunt + "leave":
            if message.guild.voice_client is None:
                await message.channel.send("接続していません。")
                return

            # 切断する
            await message.guild.voice_client.disconnect()
            await message.channel.send("切断しました。")

        elif message.content.startswith(fastHunt):

            if(not message.content.removeprefix(fastHunt).isdecimal()):
                return

            smlTxt = mojimoji.zen_to_han(message.content)

            if message.author.voice is None:
                await message.channel.send("あなたはボイスチャンネルに接続していません。")
                return

            if message.guild.voice_client is None:
                await message.author.voice.channel.connect()

            #elif message.guild.voice_client.channel != message.author.voice.channel:
                #await message.guild.voice_client.disconnect()
                #await message.author.voice.channel.connect()
            elif message.author.voice.channel.members is not None and not message.guild.me in message.author.voice.channel.members:
                await message.guild.voice_client.move_to(message.author.voice.channel)

            for num in range(allSound + 1):
                if num == allSound:
                    await message.channel.send("正しいボイスナンバーを入力してください")
                    return
                elif fastHunt + str(num) == smlTxt:
                    break

            message.guild.voice_client.stop()
            message.guild.voice_client.play(discord.FFmpegPCMAudio("voice/" + str(num) + ".mp3"))

    except Exception as e:
        print("err")
        print(e)
        return

client.run(TOKEN)
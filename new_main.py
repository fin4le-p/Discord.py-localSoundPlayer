import os
from os.path import join, dirname
import sys
import asyncio
from dotenv import load_dotenv

import discord
from discord.commands import Option

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("TOKEN")

bot = discord.Bot()
allSound: int = 220

@bot.slash_command(description="コマンドリストを表示するよ！使い方もわかるからね！")
async def list(ctx):
    await ctx.respond("ボイスの一覧，利用規約は下から見てね！\n規約・使い方：https://sara-hoshikawa.com/bot/download\nボイスリスト：https://sara-hoshikawa.com/bot/voicelist")

@bot.slash_command(description="ほちかわとおしゃべりできるよ！")
async def s(ctx, no: Option(int, "再生したい音声の番号を入力してね！")):
    
    # オプションが入力されなかったときは，ランダムで再生する（必須項目のため実装なし）
    #if no is None:
    #    no = random.randint(0, allSound)

    # 存在市内音声の番号が入力されたらreturn
    if no > allSound or no < 0:
        await ctx.respond("その番号は使えないよ！")
        return

    # ユーザーがボイスちゃんねるに接続していない場合return
    if ctx.author.voice is None:
        await ctx.respond("ボイスちゃんねるに接続してないよ？")
        return

    voice_channel= ctx.author.voice.channel

    # botが接続していない場合は接続，elif 接続しているチャンネルが違う場合は移動
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    
    # 再生していない場合のみ再生
    if not voice_client.is_playing():
        audio_source = discord.FFmpegPCMAudio('voice/' + str(no) + '.mp3')
        voice_client.play(audio_source, after=None)
    else:
        await ctx.respond("まだ喋ってるから，終わったら入力してね！")
        return

    await ctx.respond(str(no) + "番再生中♪")


#    except AttributeError:
#        await ctx.respond("ボイスちゃんねるに接続してないよ？")
#    except discord.errors.ClientException:
#        await ctx.respond("もう接続しているよ！")

@bot.slash_command(description="切断するよ！")
async def leave(ctx):
    # Botが接続していないのに切断コマンドが走った時はreturn
    if ctx.guild.me.voice is None:
        await ctx.respond("接続してないよ？")
        return

    await ctx.guild.voice_client.disconnect()
    await ctx.respond("またほちかわと遊んでね！")

bot.run(TOKEN)
from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


bot.run(token)
'''
import discord
import datetime as dt
import time
import random  # おみくじで使用
import os

TOKEN = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()  # 接続に使用するオブジェクト
shieldArray = []

from datetime import datetime, timedelta, timezone
# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')

@client.event
async def on_ready():
    """起動時に通知してくれる処理"""
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')

#@client.event  
#async def on_member_join(member):
#    for channel in member.server.channels:
#        if channel.name == 'general':
#            await client.send_message(channel, str(member.mention)+'さん！ようこそ！')

@client.event
async def on_message(message):
    
    dt1 = dt.timedelta(seconds = 0) # initialize dt1 explicitly to avoid warning
    
    """メッセージを処理"""
    if message.author.bot:  # ボットのメッセージをハネる
        return
    
#    if message.channel.id == SHIELD_CHANNEL_ID:
    if message.content == "!眠たい":
       # チャンネルへメッセージを送信
        await message.channel.send(f"{message.author.mention}さん 寝ましょう")  # f文字列（フォーマット済み文字列リテラル）

    elif message.content == "!投票":
        # リアクションアイコンを付けたい
        q = await message.channel.send("あなたは右利きですか？")
        [await q.add_reaction(i) for i in ('⭕', '❌')]  # for文の内包表記

    elif message.content == "!おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '吉', '凶', '大凶')), inline=False)
        await message.channel.send(embed=embed)

    elif message.content == "!ダイレクトメッセージ":
        # ダイレクトメッセージ送信
        dm = await message.author.create_dm()
        await dm.send(f"{message.author.mention}さんにダイレクトメッセージ")

    elif message.content == "help":
        # チャンネルへメッセージを送信
         await message.channel.send("これはシールド時間管理BOTです。\n時間を入力すればカウントダウンを始めます。\n例えば8時間なら\n   8\nと入力。もしくは\n  8:30\nのように分までの入力も受け付けます。")  # f文字列（フォーマット済み文字列リテラル）
        
    elif message.content == "list":
        shieldArray.sort(key=lambda x: x[1])
        for i in shieldArray:
            dt3 = i[1] - dt.timedelta(seconds = (time.time() - i[2])) #time until shield expire
            if dt3 <= dt.timedelta(seconds = 0):
                j = shieldArray.index(i)
                del shieldArray[j]
                continue
            dt4 = dt.datetime.now(JST) + i[1] - dt.timedelta(seconds = (time.time() - i[2])) #expected end time
            await message.channel.send(str(i[0])+"さん")
            await message.channel.send(dt4.strftime("%m/%d %H:%M ")+str(dt3).split(':',3)[0]+"時間"+str(dt3).split(':',3)[1]+"分") 

    elif ':' in message.content:
        valArray = message.content.split(':')
        dt1 = dt.timedelta(hours = int(valArray[0]), minutes = int(valArray[1]))
    else:
        dt1 = dt.timedelta(hours = int(message.content))
    
    # Check shield time up to 7days
    dt2 = dt.timedelta(hours = 168) 
    if dt1 > dt2:
        await message.channel.send("Shield time is up to 7days")
        return
            
    #check author exists in the list
    result = False
    for k in shieldArray:
        if message.author.name in k:
            result = True
            break

    if result:
        j = shieldArray.index(k)
        del shieldArray[j]

    shieldArray.append([message.author.name, dt1, time.time()])
    shieldArray.sort(key=lambda x: x[1])
    for i in shieldArray:
        dt3 = i[1] - dt.timedelta(seconds = (time.time() - i[2])) #time until shield expire
        if dt3 <= dt.timedelta(seconds = 0):
            j = shieldArray.index(i)
            del shieldArray[j]
            continue
        dt4 = dt.datetime.now(JST) + i[1] - dt.timedelta(seconds = (time.time() - i[2])) #expected end time
        await message.channel.send(str(i[0])+"さん")
        await message.channel.send(dt4.strftime("%m/%d %H:%M ")+str(dt3).split(':',3)[0]+"時間"+str(dt3).split(':',3)[1]+"分")

# botの接続と起動
# （botアカウントのアクセストークンを入れてください）
client.run(TOKEN)
'''

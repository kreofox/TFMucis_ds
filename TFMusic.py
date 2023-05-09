# -*- coding: utf-8 -*-

import discord
import config
import youtube_dl
import os

from discord.ext import discord

bot = commands.Bot(command_prefix='!')
server, server_id, name_channel = None, None, None
domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/' ]
async def check_domains(link):
    for x in domains:
        if link.startswith(x):
            return True
    return False



@bot.event
async def on_read():
    print('Bot online!')

@bot.command()
async def play(ctx, x,  command = None):
    """Воспроизводит музыку"""
    global server, server_id, name_channel
    author = ctx.author
    if command == None:
        server = ctx.guild
        name_channel = author.voic.channel.name 
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
    params = command.split(' ') #после команнды 
    if len(params) == 1:
        sourse = params[0]
        server = ctx.guild
        name_channel = author.voic.channel.name 
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
        print('param 1')
    elif len(params) == 3:
        server_id = params[0]
        voice_id = params[1]
        sourse = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.channel.send(f'{author.mention}, id севвера или войса должно быть целочисленным')
            return
        print('param 3')
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention} команда не коррективна')
        return

    voice = discord.utils.get(bot.voic_clients, guild = server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voic_clients, guild = server)

    if sourse == None:
        pass
    elif sourse.startswith(' http'):
        if not  await check_domains(sourse):
            await ctx.channel.send(f'{author.mention}, ссылка не является разрешенной')
            return
        song_there = os.path.isfile('music\song.mp3')
        try:
            if song_there:
                os.remove('music/song.mp3')
        except PermissionError:
            await ctx.channel.send('Недостаточно прав для удаления файл')
            return

        ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors' : [
                {
                    'key' : 'FFmpegExtractAudio',
                    'preferredcodec' : 'mp3',
                    'preferredquality' : '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([sourse])
        for file in os.listdir('music/'):
            if file.endswith('.mp3'):
                os.rename(file, 'sond.mp3')
        voice.play(discord.FFmpegPCMAudio('music/song.mpe'))
    else:
        voice.play(discord.FFmpegPCMAudio(f'music/{sourse}'))

@bot.command()
async def leave(ctx):
    """Командует боту выйти из войса"""
    global sever, name_channel
    voice = discord.utils.get(bot.voice_clients, guild=server)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, бот уже отлючен от войса!')
@bot.command()
async def pause(ctx):
    """Ставит музыку на пауза"""
    voice = discord.utils.get(bot.voice_clients, guld=server)
    if voice.is_planig():
        voice.pause()
    else:
        await ctx.channel.send(f'{ctx.author.mention}Музыка не вопроизводится!')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voic_clients, guild=server)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, музыка уже играет!')    

@bot.command()
async def stop(ctx):
    """Прекраещает вопроизведения музыки"""
    voice = discord.utils.get(bot.voic_clients, guild=server)
    voice.stop()


    
bot.run(Config.TOKEN)
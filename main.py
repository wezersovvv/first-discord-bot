import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import aiohttp

# intents 
inteny = discord.Intents.default()
inteny.members = True

# bot prefix
PREFIX = r'!'

#bot token
TOKEN = ('token')
 
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

#COMMANDS

#ping command to check if bot is online
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

#say command to make the bot say something
@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)

#embed command to make the bot send an embed
@bot.command()
async def embed(ctx, *, arg):
    embed = discord.Embed(title="Embed", description=arg, color=0xeee657)
    embed.set_footer(text="This is a footer!")
    embed.set_author(name="Author Name", icon_url=bot.user.avatar_url)
    embed.add_field(name="Field1", value="hi", inline=True)
    embed.add_field(name="Field2", value="hi2", inline=True)
    await ctx.send(embed=embed)

#avatar command to get the avatar of a user
@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    userAvatar = member.avatar_url
    await ctx.send(userAvatar)

#serverinfo command to get info about the server
@bot.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Владелец:", value=owner, inline=True)
    embed.add_field(name="ID сервера:", value=id, inline=True)
    embed.add_field(name="Регион:", value=region, inline=True)
    embed.add_field(name="Количество участников:", value=memberCount, inline=True)

    await ctx.send(embed=embed)

#userinfo command to get info about a user
@bot.command()
async def userinfo(ctx, member: discord.Member):
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"Информация о {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Запросил {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Имя:", value=member.display_name, inline=False)

    embed.add_field(name="Создан аккаунт:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(name="Присоединился к серверу:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

    embed.add_field(name=f"Роли ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Высшая роль:", value=member.top_role.mention, inline=False)

    await ctx.send(embed=embed)

#kick command to kick a user
@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Пользователь {member.mention} был кикнут!')

#ban command to ban a user
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Пользователь {member.mention} был забанен!')

#unban command to unban a user
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Пользователь {user.mention} был разбанен!')
            return

#clear command to clear messages
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="Список команд:", color=0xeee657)

    embed.add_field(name="ping", value="Проверка бота", inline=False)
    embed.add_field(name="say", value="Сказать что-то", inline=False)
    embed.add_field(name="embed", value="Создать embed", inline=False)
    embed.add_field(name="avatar", value="Получить аватарку пользователя", inline=False)
    embed.add_field(name="serverinfo", value="Получить информацию о сервере", inline=False)
    embed.add_field(name="userinfo", value="Получить информацию о пользователе", inline=False)
    embed.add_field(name="kick", value="Кикнуть пользователя", inline=False)
    embed.add_field(name="ban", value="Забанить пользователя", inline=False)
    embed.add_field(name="unban", value="Разбанить пользователя", inline=False)
    embed.add_field(name="clear", value="Очистить чат", inline=False)

    await ctx.send(embed=embed)

#EVENTS

@bot.event()
async def on_member_join(member):
    print(f'{member} присоеденился к серверу.')

@bot.event()
async def on_member_remove(member):
    print(f'{member} покинул сервер.')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Команда не найдена!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Укажите аргумент!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('У вас недостаточно прав!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send('У бота недостаточно прав!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Эта команда на кулдауне! Попробуйте через {round(error.retry_after, 2)} секунд.')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send('Пользователь не найден!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send('Роль не найдена!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.ChannelNotFound):
        await ctx.send('Канал не найден!')

@bot.event()
async def on_command_error(ctx, error):
    if isinstance(error, commands.EmojiNotFound):
        await ctx.send('Эмодзи не найдено!')

bot.run(TOKEN)



import io
import os

from discord import File
from discord.ext import commands
from discord.member import Member

import config


@commands.command(help='Export a .csv of users who joined a joinable channel')
@commands.has_role(config.role['global_mod'])
async def userexport(ctx, channel_id: int = 0):
    try:
        channel = next(ch for ch in ctx.guild.channels if ch.id == channel_id)
    except StopIteration:
        channel = ctx.channel
    output = io.StringIO()
    output.write(f"id,name{os.linesep}")
    joined_members = list(filter(
        lambda o: type(o[0]) is Member and not o[0].bot and o[1].read_messages,
        channel.overwrites.items()
    ))
    if not bool(joined_members):
        await ctx.send(f'Could not find any users in that channel {ctx.author.mention}')
        return
    for overwrite in joined_members:
        output.write(f'{overwrite[0].id},{overwrite[0].name}{os.linesep}')

    binary = io.BytesIO(output.getvalue().encode('utf-8'))
    await ctx.send(f'Here is your export {ctx.author.mention}', file=File(binary, f"{channel.name}.csv"))
    print(f"{ctx.author} exported users for channel {channel}")


def setup(bot):
    bot.add_command(userexport)

""" brayne module """
from datetime import datetime
from os import name as os_name
from platform import platform, python_version, system

from discord import Color, CustomActivity, Embed, __version__
from discord.ext import commands
from gpiozero import CPUTemperature
from psutil import (boot_time, cpu_count, cpu_freq, cpu_percent,
                    disk_usage, virtual_memory)


class Brayne(commands.Cog):
    """ Brayne class """

    def __init__(self, bot):
        self.bot = bot
        self.ass = self.bot.get_cog('Assets')
        self.connected_time = 0

    @commands.command(aliases=['about', 'info', 'ver', 'version'])
    async def brayne(self, ctx):
        """
        Sends information about Bronson's BrAyNe

        Builds & sends an embed of information retrieved from
        the system that the bot is currently running on, formatting
        each number to display 2 decimal places, & displaying values
        in F, GB, GHz

        Usage: <prefix>brayne
        Aliases: about, info, ver, version
        """
        embed = Embed(
            description=self._get_platform_info(), color=Color.blue())
        embed.add_field(
            name='__CPU__:', value=self._get_cpu_info(), inline=True)
        embed.add_field(
            name='__Memory__:', value=self._get_memory_info(), inline=True)
        embed.add_field(
            name='__Disk__:', value=self._get_disk_info(), inline=True)
        embed.set_author(
            name="Bronson's BrAyNe", icon_url=await self.ass.get_url('bbb'))
        embed.set_thumbnail(url=await self.ass.get_url('brayne'))

        await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        """ called when the bot is online & ready """
        self.connected_time = datetime.now()
        await self.bot.change_presence(
            activity=CustomActivity(name='420.69-1.2.1'))

    def _get_platform_info(self):
        """ get platform info  """
        booted_time = datetime.fromtimestamp(boot_time())

        platform_info = (
            '**Bot version**: 420.69-1.2.1\n'
            '**GitHub**: '
            '[/mdf-gh/bronson](https://www.github.com/mdf-gh/bronson)\n\n'
            f'**Python version**: {python_version()}\n'
            f'**discord.py API version**: {__version__}\n\n'
            f'**OS**: {platform()} ({os_name})\n\n'
            f'**Bot uptime**: {self._get_uptime(self.connected_time)}\n'
            f'**System uptime**: {self._get_uptime(booted_time)}'
        )
        return platform_info

    def _get_cpu_info(self):
        """ get cpu info """
        # get cpu temp if on linux (raspberry pi)
        if system().lower() == "linux":
            cpu_temp = CPUTemperature()
            cpu_temp_f = cpu_temp.temperature * (9 / 5) + 32
            cpu_temp_f = f'{cpu_temp_f:.2f} °F'
        else:
            cpu_temp_f = 'N/A'

        cpu_info = (
            f'**Usage**: {cpu_percent(interval=1):.2f}%\n'
            f'**Core/Freq**: {cpu_count(logical=False)}x @ '
            f'{cpu_freq().current / 1000:.2f} GHz '
            f'(***max*** *{cpu_freq().max / 1000:.2f} GHz*)\n'
            f'**Temperature**: {cpu_temp_f}'
        )
        return cpu_info

    def _get_memory_info(self):
        """ get memory info """
        memory_info = (
            f'**Used**: {virtual_memory().used / (1024 ** 3):.2f} GB\n'
            f'**Total**: {virtual_memory().total / (1024 ** 3):.2f} GB\n'
            f'({virtual_memory().percent:.2f}%)'
        )
        return memory_info

    def _get_disk_info(self):
        """ get disk info """
        disk_info = (
            f'**Used**: {disk_usage('/').used / (1024 ** 3):.2f} GB\n'
            f'**Total**: {disk_usage('/').total / (1024 ** 3):.2f} GB\n'
            f'({disk_usage('/').percent:.2f}%)'
        )
        return disk_info

    def _get_uptime(self, start_time):
        """ get uptime info for bot or system """
        delta = datetime.now() - start_time

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime = f'{days}d, {hours}h, {minutes}m, {seconds}s'
        return uptime

    @brayne.error
    async def brayne_error(self, ctx, error):
        """ handles brayne errors """
        await ctx.reply(f'**Error**: {error}')


async def setup(bot):
    """ adds class to bot's cog system """
    await bot.add_cog(Brayne(bot))

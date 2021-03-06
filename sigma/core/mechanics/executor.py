# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio

import discord

from sigma.core.mechanics.logger import create_logger


class ExecutionClockwork(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Threader')
        self.queue = asyncio.Queue()
        self.bot.loop.create_task(self.queue_loop())
        self.processed = 0

    async def get_cmd_and_args(self, message: discord.Message, args: list, mention: bool = False):
        args = list(filter(lambda a: a != '', args))
        if mention:
            if args:
                cmd = args.pop(0).lower()
            else:
                cmd = None
        else:
            pfx = await self.bot.db.get_prefix(message)
            cmd = args.pop(0)[len(pfx):].lower()
        return cmd, args

    def clean_self_mentions(self, message: discord.Message):
        for mention in message.mentions:
            if mention.id == self.bot.user.id:
                message.mentions.remove(mention)
                break

    async def command_runner(self, message: discord.Message):
        prefix = await self.bot.db.get_prefix(message)
        if message.content.startswith(prefix):
            args = message.content.split(' ')
            cmd, args = await self.get_cmd_and_args(message, args)
        elif message.content.startswith(self.bot.user.mention):
            args = message.content.split(' ')[1:]
            self.clean_self_mentions(message)
            cmd, args = await self.get_cmd_and_args(message, args, mention=True)
        elif message.content.startswith(f'<@!{self.bot.user.id}>'):
            args = message.content.split(' ')[1:]
            cmd, args = await self.get_cmd_and_args(message, args, mention=True)
        else:
            cmd = None
            args = []
        if cmd:
            cmd = self.bot.modules.alts.get(cmd) if cmd in self.bot.modules.alts else cmd
            command = self.bot.modules.commands.get(cmd)
            if command:
                task = command, message, args
                await self.queue.put(task)

    async def event_runner(self, event_name: str, *args):
        if self.bot.ready:
            if event_name in self.bot.modules.events:
                for event in self.bot.modules.events[event_name]:
                    task = event, *args
                    await self.queue.put(task)

    async def queue_loop(self):
        while True:
            if self.bot.ready:
                item, *args = await self.queue.get()
                self.bot.loop.create_task(item.execute(*args))
                self.processed += 1
            else:
                await asyncio.sleep(1)

﻿# Apex Sigma: The Database Giant Discord Bot.
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

import json
import secrets

import aiohttp
import discord


async def boobs(cmd, message, args):
    api_base = 'http://api.oboobs.ru/boobs/'
    number = secrets.randbelow(10303) + 1
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.oboobs.ru/' + data['preview']
    model = data['model']
    if not model:
        model = 'Unknown'
    rank = data['rank']
    boobs_icon = 'http://fc01.deviantart.net/fs71/f/2013/002/d/9/_boobs_icon_base__by_laurypinky972-d5q83aw.png'
    embed = discord.Embed(color=0xF9F9F9)
    embed.set_author(name='Open Boobs', icon_url=boobs_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await message.channel.send(None, embed=embed)

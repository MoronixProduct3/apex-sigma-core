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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand

api_endpoint = 'http://api.royal-destiny.com/syndicates'
royaldestiny_color = 0xe88f03
royaldestiny_logo = 'https://i.imgur.com/m4ngGxb.png'

async def wfsyndicates(cmd: SigmaCommand, message: discord.Message, args: list):
    initial_response = discord.Embed(color=0xFFCC66, title='🔬 Processing...')
    init_resp_msg = await message.channel.send(embed=initial_response)
    response = discord.Embed(color=royaldestiny_color)
    response.set_author(name='Best syndicate offerings:')
    async with aiohttp.ClientSession() as session:
        async with session.get(api_endpoint) as data:
            page_data = await data.read()
            data = json.loads(page_data)
    if data['syndicates']:
        for syndicate in data['syndicates']:
            items = ''
            for item in syndicate['offerings'][0:3]:
                items += f'__{item["name"]}:__ {item["platPrice"]}'
            response.add_field(name=syndicate['name'], value=items)
    try:
        await init_resp_msg.edit(embed=response)
    except discord.NotFound:
        pass
    
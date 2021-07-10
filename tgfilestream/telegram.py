# tgfilestream - A Telegram bot that can stream Telegram files to users over HTTP.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.'
import logging

from telethon import TelegramClient, events
from starkfunc import check_if_subbed
from configs import Config

from .paralleltransfer import ParallelTransferrer
from .config import (
    session_name,
    api_id,
    api_hash,
    public_url,
    start_message,
    group_chat_message
)
from .util import pack_id, get_file_name

log = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)
transfer = ParallelTransferrer(client)

@client.on(events.NewMessage(pattern="^/start$"))

async def hmm(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	
@client.on(events.NewMessage)
async def handle_message(evt: events.NewMessage.Event) -> None:
        if not evt.is_private:
        await evt.reply(group_chat_message)
        return
    if not evt.file:
        await evt.reply(start_message)
        return
    url = public_url / str(pack_id(evt)) / get_file_name(evt)
    await evt.reply(f"Link to download file: [get_file_name(evt)]{url}")
    log.info(f"Replied with link for {evt.id} to {evt.from_id} in {evt.chat_id}")
    log.debug(f"Link to {evt.id} in {evt.chat_id}: {url}")

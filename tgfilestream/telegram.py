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
from telegram.utils.helpers import escape_markdown as es


from .paralleltransfer import ParallelTransferrer
from .config import (
    session_name,
    api_id,
    api_hash,
    public_url,
    group_chat_message
)
from .util import pack_id, get_file_name

log = logging.getLogger(__name__)

def start_msg(name):
    msg = f"""*Hey {es(name,version=2)}*\n\n*Send any document 📁🗂️🎥🎤🖼️ to get direct download link.*"""
    return msg


def start(update, context):
    fname = update.message.chat.first_name
    update.message.reply_text(
        start_msg(fname), parse_mode="MarkdownV2")

client = TelegramClient(session_name, api_id, api_hash)
transfer = ParallelTransferrer(client)
      	
@client.on(events.NewMessage)
async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        await evt.reply(group_chat_message)
        return
    url = public_url / str(pack_id(evt)) / get_file_name(evt)
    await evt.reply(f"Link to download file: [Click here]({url})")
    log.info(f"Replied with link for {evt.id} to {evt.from_id} in {evt.chat_id}")
    log.debug(f"Link to {evt.id} in {evt.chat_id}: {url}")

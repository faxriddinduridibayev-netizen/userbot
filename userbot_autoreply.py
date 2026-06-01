"""
USERBOT AUTO-REPLY — Railway uchun
===================================
Muhit o'zgaruvchilari (Railway → Variables):
    API_ID        → my.telegram.org dan
    API_HASH      → my.telegram.org dan
    SESSION_STRING → quyidagi session_gen.py dan oling
"""

import asyncio
import os
from datetime import datetime, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import User

# ─── SOZLAMALAR (Railway Variables dan o'qiladi) ─────────────
API_ID         = int(os.environ["API_ID"])
API_HASH       = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# ─── XABAR MATNI ─────────────────────────────────────────────
AWAY_MESSAGE = (
    "Salom! 👋 Hozir aloqada emasman.\n"
    "Tez orada javob beraman. Muhim bo'lsa, qo'ng'iroq qiling. 🙏"
)

# ─── VAQT SOZLAMALARI ────────────────────────────────────────
ALWAYS_AWAY      = True
AWAY_FROM        = time(22, 0)
AWAY_TO          = time(9,  0)
COOLDOWN_SECONDS = 3600

# ─────────────────────────────────────────────────────────────

client   = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
sent_log: dict[int, datetime] = {}


def is_away_time() -> bool:
    if ALWAYS_AWAY:
        return True
    now = datetime.now().time()
    if AWAY_FROM <= AWAY_TO:
        return AWAY_FROM <= now <= AWAY_TO
    return now >= AWAY_FROM or now <= AWAY_TO


def can_reply(user_id: int) -> bool:
    last = sent_log.get(user_id)
    if last is None:
        return True
    return (datetime.now() - last).total_seconds() >= COOLDOWN_SECONDS


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_message(event):
    sender: User = await event.get_sender()
    if sender.bot:
        return
    if not is_away_time():
        return
    if not can_reply(sender.id):
        return

    await event.reply(AWAY_MESSAGE)
    sent_log[sender.id] = datetime.now()

    name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
    print(f"[{datetime.now():%H:%M:%S}] Javob yuborildi → {name} (ID: {sender.id})")


async def main():
    print("Userbot ishga tushdi! To'xtatish: Ctrl+C")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())

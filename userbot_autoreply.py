"""
USERBOT AUTO-REPLY — Shaxsiy akkount uchun
==========================================
O'rnatish:
    pip install telethon

Ishga tushirish:
    python userbot_autoreply.py

Birinchi ishga tushirishda Telegram SMS kodi so'raladi.
"""

import asyncio
from datetime import datetime, time
from telethon import TelegramClient, events
from telethon.tl.types import User

# ─── SOZLAMALAR ──────────────────────────────────────────────
# https://my.telegram.org/apps dan oling
API_ID   = 35518453          # <-- o'zgartiring
API_HASH = "e235446080a86aa8ccdbff7b964c3819"   # <-- o'zgartiring

# ─── XABAR MATNI ─────────────────────────────────────────────
AWAY_MESSAGE = (
    "Salom! 👋 Hozir aloqada emasman.\n"
    "Tez orada javob beraman. Muhim bo'lsa, qo'ng'iroq qiling. 🙏"
)

# ─── QAYSI VAQTLARDA AKTIV BO'LSIN? ─────────────────────────
# True  → doim javob beradi
# False → faqat quyidagi vaqt oralig'ida
ALWAYS_AWAY = True
AWAY_FROM   = time(22, 0)   # 22:00 dan
AWAY_TO     = time(9,  0)   # 09:00 gacha (tun bo'yi)

# ─── KIMGA JAVOB BERSIN? ─────────────────────────────────────
REPLY_TO_ALL     = True   # False bo'lsa, faqat quyidagi ro'yxatga
ALLOWED_USER_IDS = []     # masalan: [123456789, 987654321]

# ─── QAYTA YUBORMASLIK MUDDATI (sekund) ──────────────────────
COOLDOWN_SECONDS = 3600   # bir odamga soatiga bir marta

# ─────────────────────────────────────────────────────────────

client   = TelegramClient("away_session", API_ID, API_HASH)
sent_log: dict[int, datetime] = {}   # {user_id: last_sent_time}


def is_away_time() -> bool:
    """Hozir 'yo'q' vaqtimi?"""
    if ALWAYS_AWAY:
        return True
    now = datetime.now().time()
    if AWAY_FROM <= AWAY_TO:
        return AWAY_FROM <= now <= AWAY_TO
    # Tun bo'yi: masalan 22:00 → 09:00
    return now >= AWAY_FROM or now <= AWAY_TO


def can_reply(user_id: int) -> bool:
    """Bu foydalanuvchiga hali javob berilmaganmi?"""
    last = sent_log.get(user_id)
    if last is None:
        return True
    elapsed = (datetime.now() - last).total_seconds()
    return elapsed >= COOLDOWN_SECONDS


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_message(event):
    """Shaxsiy xabar kelganda ishga tushadi."""
    sender: User = await event.get_sender()

    # Botlardan kelgan xabarlarga javob berma
    if sender.bot:
        return

    # Faqat ruxsat etilgan foydalanuvchilarga javob ber
    if not REPLY_TO_ALL and sender.id not in ALLOWED_USER_IDS:
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
    print("=" * 50)
    print("  Userbot ishga tushdi!")
    print(f"  Rejim: {'DOIM YO\'Q' if ALWAYS_AWAY else f'{AWAY_FROM} – {AWAY_TO}'}")
    print("  To'xtatish uchun: Ctrl+C")
    print("=" * 50)
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())

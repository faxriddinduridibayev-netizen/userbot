"""
SESSION STRING GENERATORI
==========================
Bir marta o'z kompyuteringizda ishga tushiring.
Natijada SESSION_STRING chiqadi — uni Railway ga kiriting.

O'rnatish:  pip install telethon
Ishlatish:  python session_gen.py
"""

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID   = input("API_ID kiriting: ").strip()
API_HASH = input("API_HASH kiriting: ").strip()

with TelegramClient(StringSession(), int(API_ID), API_HASH) as client:
    session = client.session.save()

print("\n" + "=" * 60)
print("SESSION_STRING (quyidagini Railway ga kiriting):")
print("=" * 60)
print(session)
print("=" * 60)
print("\nDIQQAT: Bu qatorni hech kimga ko'rsatmang!")

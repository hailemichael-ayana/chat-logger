import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_account")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

MEDIA_DIR = "downloads"
os.makedirs(MEDIA_DIR, exist_ok=True)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def log_messages(event):
    sender = await event.get_sender()
    
    if event.is_group or event.chat_id < 0 or sender.bot:
        return

    sender_name = sender.first_name or "Unknown"
    sender_info = f"{sender_name} (@{sender.username or sender.id})"

    if event.text:
        await client.send_message(LOG_CHANNEL_ID, f"**{sender_info}**:\n{event.text}")

    if event.media:
        file_path = await event.download_media(file=MEDIA_DIR)
        await client.send_file(LOG_CHANNEL_ID, file_path, caption=f"**{sender_info}**")

client.start()
client.run_until_disconnected()

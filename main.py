import discum
import os
from flask import Flask
from threading import Thread

# --- Keep Alive Sunucu Kodu ---
app = Flask('')

@app.route('/')
def home():
    return "Bot çalışıyor."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- Sunucu Kodu Bitişi ---


# --- discum Bot Kodu ---
TOKEN = os.environ.get('TOKEN')
GUILD_ID = os.environ.get('GUILD_ID')
VOICE_CHANNEL_ID = os.environ.get('VOICE_CHANNEL_ID')

if not all([TOKEN, GUILD_ID, VOICE_CHANNEL_ID]):
    print("[!] HATA: TOKEN, GUILD_ID, veya VOICE_CHANNEL_ID ortam değişkenleri (Secrets) ayarlanmamış.")
    exit()

bot = discum.Client(
    token=TOKEN,
    log={
        "console": True,
        "file": False
    },
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
)


def join_voice(guild_id, channel_id):
    payload = {
        "op": 4,
        "d": {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "self_mute": True,
            "self_deaf": True,
        }
    }
    bot.gateway.send(payload)


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready:
        # HATA ALINAN SATIRI DÜZELTİYORUZ
        # 'user' bilgisini session'dan değil, doğrudan READY olayının verisinden ('resp.d') alıyoruz.
        user = resp.d['user'] 
        print(f"[✓] Gateway'e bağlanıldı: {user['username']}#{user['discriminator']}")
        
        print(f"[!] Ses kanalına bağlanılıyor -> Sunucu: {GUILD_ID}, Kanal: {VOICE_CHANNEL_ID}")
        join_voice(GUILD_ID, VOICE_CHANNEL_ID)

# Projeyi başlat
keep_alive()
print("[!] discum botu başlatılıyor...")
bot.gateway.run(auto_reconnect=True)

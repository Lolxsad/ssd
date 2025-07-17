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
# ID'leri string olarak kullanmak daha güvenlidir.
GUILD_ID = os.environ.get('GUILD_ID')
VOICE_CHANNEL_ID = os.environ.get('VOICE_CHANNEL_ID')

# Ortam değişkenlerinin dolu olup olmadığını kontrol et
if not all([TOKEN, GUILD_ID, VOICE_CHANNEL_ID]):
    print("[!] HATA: TOKEN, GUILD_ID, veya VOICE_CHANNEL_ID ortam değişkenleri (Secrets) ayarlanmamış.")
    exit()

# discum'un build number hatasını düzeltmek için User-Agent belirtiyoruz.
# Bu, kütüphanenin doğru versiyon bilgisiyle çalışmasına yardımcı olur.
bot = discum.Client(
    token=TOKEN,
    log={
        "console": True,
        "file": False
    },
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
)


def join_voice(guild_id, channel_id):
    # Bu, Discord'un ses durumu güncelleme komutudur (Opcode 4).
    payload = {
        "op": 4,
        "d": {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "self_mute": True,  # Kendini sustur
            "self_deaf": True,   # Kendini sağırlaştır
        }
    }
    # Hazırladığımız komutu doğrudan gateway'e gönderiyoruz.
    bot.gateway.send(payload)


# Olay dinleyicisini bu şekilde tanımlamak daha güvenilir olabilir.
@bot.gateway.command
def on_ready(resp):
    # Bot 'READY' veya 'READY_SUPPLEMENTAL' olayını aldığında...
    if resp.event.ready or resp.event.ready_supplemental:
        user = bot.gateway.session.user
        print(f"[✓] Gateway'e bağlanıldı: {user['username']}#{user['discriminator']}")
        
        print(f"[!] Ses kanalına bağlanılıyor -> Sunucu: {GUILD_ID}, Kanal: {VOICE_CHANNEL_ID}")
        # Ses kanalına katılma fonksiyonunu çağır
        join_voice(GUILD_ID, VOICE_CHANNEL_ID)

# Projeyi başlat
keep_alive()
print("[!] discum botu başlatılıyor...")
# auto_reconnect=True, botun bağlantısı koparsa yeniden bağlanmasını sağlar.
bot.gateway.run(auto_reconnect=True)

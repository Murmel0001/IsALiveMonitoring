import time
import requests

# =========================
# KONFIGURATION
# =========================

# URLs zum Überwachen (mehrere mit Komma trennen)
URLS = [
    "https://test.luxos-vt.de"
]

# Intervall in Sekunden
INTERVAL = 60

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "8369846397:AAG-Lfo3cBHp6GjB5Voa-PJNPlQa6VWgH6k"
TELEGRAM_CHAT_ID = "-5281025997"  # Gruppen-ID oder Chat-ID

# =========================
# MONITORING
# =========================

last_status = {}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Telegram Nachricht konnte nicht gesendet werden: {e}", flush=True)

def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        reachable = response.status_code < 500
        status_text = f"HTTP {response.status_code}"
    except requests.exceptions.RequestException:
        reachable = False
        status_text = "nicht erreichbar"

    previous = last_status.get(url)

    if reachable:
        print(f"[OK]   {url} ({status_text})", flush=True)
        if previous is False:
            send_telegram_message(
                f"✅ *Wieder erreichbar*\n{url}\nStatus: {status_text}"
            )
    else:
        print(f"[DOWN] {url} {status_text}", flush=True)
        if previous is not False:
            send_telegram_message(
                f"🚨 *Server DOWN*\n{url}\nStatus: {status_text}"
            )

    last_status[url] = reachable


# =========================
# START MONITORING
# =========================

print("🚀 Starte URL-Monitoring", flush=True)
print(f"⏱️  Intervall: {INTERVAL}s", flush=True)
print("🌍 URLs:", flush=True)
for u in URLS:
    print(f" - {u}", flush=True)
print("-" * 40, flush=True)

while True:
    for url in URLS:
        check_url(url)
    print("-" * 40, flush=True)
    time.sleep(INTERVAL)

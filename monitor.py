import time
import requests
import os

# =========================
# ENV CONFIG
# =========================

URLS_ENV = os.getenv("URLS", "")
URLS = [u.strip() for u in URLS_ENV.split(",") if u.strip()]

INTERVAL = int(os.getenv("INTERVAL", "30"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not URLS:
    raise RuntimeError("ENV URLS ist leer! Mindestens eine URL angeben.")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("ENV TELEGRAM_BOT_TOKEN fehlt!")

if not TELEGRAM_CHAT_ID:
    raise RuntimeError("ENV TELEGRAM_CHAT_ID fehlt!")

# =========================
# MONITORING LOGIC
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
    requests.post(url, json=payload, timeout=5)

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

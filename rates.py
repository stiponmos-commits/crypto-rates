import os, requests
from datetime import datetime, timezone, timedelta

TOKEN = os.environ["BOT_TOKEN"]
CHAT  = "@newscrman"          # ← username твоего канала
API   = "https://api.telegram.org/bot" + TOKEN
MARK  = "📊 АКТУАЛЬНЫЕ КУРСЫ"

def call(m, d):
    return requests.post(API + "/" + m, json=d, timeout=20).json()

b = requests.get("https://api.coingecko.com/api/v3/simple/price",
    params={"ids": "bitcoin", "vs_currencies": "usd",
            "include_24hr_change": "true"}, timeout=20).json()["bitcoin"]
u = requests.get("https://www.cbr-xml-daily.ru/daily_json.js",
                 timeout=20).json()["Valute"]["USD"]["Value"]

p, c = b["usd"], b["usd_24h_change"]
now = datetime.now(timezone(timedelta(hours=3)))
rub = f"{p*u:,.0f}".replace(",", " ")

t = (MARK + "\n\n"
     f"💵 Доллар (ЦБ РФ): {u:.2f} ₽\n"
     f"₿ Биткоин: ${p:,.0f}\n"
     f"     ≈ {rub} ₽\n"
     f"{'🟢' if c >= 0 else '🔴'} BTC за 24ч: {c:+.2f}%\n\n"
     f"🕒 Обновлено: {now:%d.%m.%Y %H:%M} МСК")

pin = call("getChat", {"chat_id": CHAT}).get("result", {}).get("pinned_message") or {}

if pin.get("text", "").startswith(MARK):
    r = call("editMessageText", {"chat_id": CHAT,
                                 "message_id": pin["message_id"], "text": t})
else:
    r = call("sendMessage", {"chat_id": CHAT, "text": t})
    if r.get("ok"):
        call("pinChatMessage", {"chat_id": CHAT,
                                "message_id": r["result"]["message_id"],
                                "disable_notification": True})
print(r)
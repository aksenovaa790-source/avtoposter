#!/usr/bin/env python3
"""Правка уже опубликованного текстового сообщения в канале: python publisher/tg_edit.py <message_id> <файл с текстом>"""
import html, os, re, sys, requests

def md_to_html(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)
    t = re.sub(r"__(.+?)__", r"<i>\1</i>", t, flags=re.S)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)
    return t

mid, path = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read().strip()
base = f"https://api.telegram.org/bot{os.environ['TG_BOT_TOKEN']}"
r = requests.post(f"{base}/editMessageText", data={"chat_id": os.environ["TG_CHANNEL"], "message_id": mid,
                  "text": md_to_html(text), "parse_mode": "HTML"}, timeout=60).json()
print("OK" if r.get("ok") else f"Ошибка: {r.get('description')}")
sys.exit(0 if r.get("ok") else 1)

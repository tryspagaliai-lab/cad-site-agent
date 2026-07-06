#!/usr/bin/env python3
"""AI Research Digest — standalone (be n8n). Surenka naujienas, Gemini santrauka -> Telegram.
Aplinka: TELEGRAM_TOKEN, CHAT_ID, GEMINI_KEY (is /root/ai_digest.env)."""
import os, json, re, html, urllib.request, xml.etree.ElementTree as ET

TG = os.environ["TELEGRAM_TOKEN"]
CHAT = os.environ["CHAT_ID"]
GEM = os.environ["GEMINI_KEY"]
UA = {"User-Agent": "Mozilla/5.0 (AI-Digest)"}

FEEDS = [
    ("arXiv cs.AI", "https://rss.arxiv.org/rss/cs.AI"),
    ("arXiv cs.LG", "https://rss.arxiv.org/rss/cs.LG"),
    ("arXiv cs.CL", "https://rss.arxiv.org/rss/cs.CL"),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml"),
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("Google AI", "https://blog.google/technology/ai/rss/"),
    ("Meta AI", "https://ai.meta.com/blog/rss/"),
    ("Microsoft Research", "https://www.microsoft.com/en-us/research/feed/"),
    ("MIT News AI", "https://news.mit.edu/rss/topic/artificial-intelligence2"),
    ("Berkeley BAIR", "https://bair.berkeley.edu/blog/feed.xml"),
    ("Stanford HAI", "https://hai.stanford.edu/rss.xml"),
    ("Import AI", "https://importai.substack.com/feed"),
    ("Simon Willison", "https://simonwillison.net/atom/everything/"),
]
PER_FEED = 5


def get(url, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def parse_feed(name, xml_bytes):
    out = []
    root = ET.fromstring(xml_bytes)
    tag = lambda e: e.tag.split("}")[-1]
    # RSS
    items = root.findall(".//item")
    if items:
        for it in items[:PER_FEED]:
            t = l = ""
            for c in it:
                if tag(c) == "title": t = clean(c.text)
                elif tag(c) == "link": l = (c.text or "").strip()
            if t and l:
                out.append((name, t, l))
        return out
    # Atom
    for it in root.findall(".//{*}entry")[:PER_FEED]:
        t = l = ""
        for c in it:
            if tag(c) == "title": t = clean(c.text)
            elif tag(c) == "link":
                href = c.get("href")
                if href and (not c.get("rel") or c.get("rel") == "alternate") and not l:
                    l = href
        if t and l:
            out.append((name, t, l))
    return out


def collect():
    rows = []
    for name, url in FEEDS:
        try:
            rows += parse_feed(name, get(url))
        except Exception as e:
            print(f"  skip {name}: {e}")
    # new HF models
    try:
        data = json.loads(get("https://huggingface.co/api/models?sort=createdAt&direction=-1&limit=8"))
        for m in data:
            mid = m.get("modelId") or m.get("id")
            if mid:
                rows.append(("HF nauji modeliai", mid, "https://huggingface.co/" + mid))
    except Exception as e:
        print(f"  skip HF models: {e}")
    return rows


def summarize(rows):
    listing = "\n".join(f"- [{s}] {t} | {l}" for s, t, l in rows)
    prompt = (
        "Tu esi AI srities naujienu analitikas. Zemiau - naujienos is pirmaujanciu pasaulio AI "
        "laboratoriju, universitetu ir bendruomenes saltiniu (arXiv, Hugging Face, OpenAI, DeepMind, "
        "Google, Meta, Microsoft Research, MIT, Stanford, Berkeley ir kt.).\n\n"
        "Uzduotis: parenk dienos ataskaita LIETUVIU kalba. Struktura (praleisk sekcija, jei nieko nera):\n"
        "NAUJI MODELIAI IR LEIDIMAI\nAGENTAI, IRANKIAI, HARNESS / SKILLS\nSVARBIAUSI TYRIMAI (arXiv)\n"
        "LABORATORIJOS IR UNIVERSITETAI\nTOP 3 DIENOS IVYKIAI\n\n"
        "Kiekvienam irasui: pavadinimas, 1-2 sakiniai kodel svarbu, ir nuoroda atskiroje eiluteje. "
        "arXiv sekcijoje max 5 reiksmingiausi. Rasyk paprastu tekstu be Markdown zenklu. Iki ~3500 simboliu.\n\n"
        "NAUJIENOS:\n" + listing
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 3000, "temperature": 0.4, "thinkingConfig": {"thinkingBudget": 0}},
    }).encode()
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent",
        data=body, headers={"Content-Type": "application/json", "x-goog-api-key": GEM},
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=120).read())
    parts = resp["candidates"][0]["content"]["parts"]
    return "\n".join(p.get("text", "") for p in parts).strip()


def send(text):
    for i in range(0, len(text), 3800):
        chunk = text[i:i + 3800]
        data = urllib.parse.urlencode({"chat_id": CHAT, "text": chunk, "disable_web_page_preview": "true"}).encode()
        urllib.request.urlopen(f"https://api.telegram.org/bot{TG}/sendMessage", data=data, timeout=30).read()


if __name__ == "__main__":
    import urllib.parse
    rows = collect()
    print(f"surinkta {len(rows)} naujienu")
    if not rows:
        send("AI Digest: siandien naujienu nerasta.")
        raise SystemExit(0)
    try:
        summary = summarize(rows)
    except Exception as e:
        summary = "Nepavyko sugeneruoti AI santraukos (" + str(e) + "). Naujienos:\n\n" + \
                  "\n".join(f"- [{s}] {t}\n  {l}" for s, t, l in rows[:30])
    import datetime
    header = "AI Research Digest\n\n"
    send(header + summary)
    print("issiusta i Telegram")

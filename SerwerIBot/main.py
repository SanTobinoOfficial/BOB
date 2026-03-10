import discord
from discord.ext import commands
import json
import random
import string
import os
import requests
import base64
from aiohttp import web
import asyncio
import re
from datetime import datetime

TOKEN              = os.environ.get("DISCORD_TOKEN", "")
JSON_FILE          = "licenses.json"
GITHUB_TOKEN       = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO_OWNER  = os.environ.get("GITHUB_REPO_OWNER", "")
GITHUB_REPO_NAME   = os.environ.get("GITHUB_REPO_NAME", "")
ADMIN_CHANNEL_ID   = int(os.environ.get("ADMIN_CHANNEL_ID", "0"))
WEBHOOK_SECRET     = os.environ.get("WEBHOOK_SECRET", "")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

activity_log = []
ws_clients: set = set()


def log_activity(action, details):
    entry = {
        "time":    datetime.now().strftime("%H:%M:%S"),
        "date":    datetime.now().strftime("%Y-%m-%d"),
        "action":  action,
        "details": details,
    }
    activity_log.insert(0, entry)
    if len(activity_log) > 200:
        activity_log.pop()
    asyncio.ensure_future(_broadcast_ws())


async def _broadcast_ws():
    dead = set()
    for ws in ws_clients:
        try:
            await ws.send_json({"type": "update"})
        except Exception:
            dead.add(ws)
    ws_clients.difference_update(dead)


def load_licenses():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_licenses(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)
    update_github_file(data)


def update_github_file(data):
    if not all([GITHUB_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME]):
        print("GitHub config missing, skipping.")
        return
    url = (f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/"
           f"{GITHUB_REPO_NAME}/contents/{JSON_FILE}")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept":        "application/vnd.github.v3+json",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        sha  = resp.json().get("sha") if resp.status_code == 200 else None
        encoded = base64.b64encode(json.dumps(data, indent=4).encode()).decode()
        payload = {"message": "Update licenses.json via Bot", "content": encoded}
        if sha:
            payload["sha"] = sha
        r = requests.put(url, headers=headers, json=payload, timeout=10)
        print(f"GitHub update: {r.status_code}")
    except Exception as e:
        print(f"Error updating GitHub: {e}")


def generate_key():
    k = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return '-'.join([k[i:i+4] for i in range(0, 16, 4)])


def parse_webhook_message(content: str) -> dict:
    """
    Parsuje wiadomości z makra AHK.
    Jedyny obsługiwany typ: NOWA AKTYWACJA
    Makro wysyła ten webhook tylko raz (kontrolowane przez sent_info.dat).
    """
    result = {}

    key_m = re.search(
        r'Klucz[:\s]+([A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4})',
        content)
    if key_m:
        result['key'] = key_m.group(1)

    hwid_m = re.search(r'HWID[:\s]+([A-F0-9\-]{30,})', content, re.IGNORECASE)
    if hwid_m:
        result['hwid'] = hwid_m.group(1).strip()

    debug_m = re.search(r'KodDebug[:\s]+([A-Z0-9]{4}-[A-Z0-9]{4})', content)
    if debug_m:
        result['debug_code'] = debug_m.group(1)

    if 'NOWA AKTYWACJA' in content:
        result['type'] = 'activation'

    return result


# ── Discord Commands ──────────────────────────────────────────────

@bot.command()
async def generate(ctx):
    data = load_licenses()
    key  = generate_key()
    data[key] = {"hwid": "", "banned": False, "note": "", "debug_code": ""}
    save_licenses(data)
    log_activity("GENERATE", f"Klucz {key} wygenerowany przez {ctx.author}")
    await ctx.send(f"Nowy klucz: `{key}`")


@bot.command()
async def ban(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["banned"] = True
    save_licenses(data)
    log_activity("BAN", f"Klucz {key} zbanowany przez {ctx.author}")
    await ctx.send(f"Klucz `{key}` zbanowany")


@bot.command()
async def unban(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["banned"] = False
    save_licenses(data)
    log_activity("UNBAN", f"Klucz {key} odbanowany przez {ctx.author}")
    await ctx.send(f"Klucz `{key}` odbanowany")


@bot.command()
async def reset(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["hwid"] = ""
    save_licenses(data)
    log_activity("RESET", f"HWID klucza {key} zresetowany przez {ctx.author}")
    await ctx.send(f"HWID klucza `{key}` zresetowany")


@bot.command()
async def assign(ctx, key, hwid):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["hwid"] = hwid
    save_licenses(data)
    log_activity("ASSIGN", f"HWID {hwid[:12]}... przypisany do {key}")
    await ctx.send(f"HWID przypisany do klucza `{key}`")


@bot.command()
async def note(ctx, key, *, text):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["note"] = text
    save_licenses(data)
    log_activity("NOTE", f"Notatka klucza {key}: {text[:40]}")
    await ctx.send(f"Notatka klucza `{key}`:\n> {text}")


@bot.command()
async def clearnote(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    data[key]["note"] = ""
    save_licenses(data)
    log_activity("NOTE", f"Notatka klucza {key} wyczyszczona przez {ctx.author}")
    await ctx.send(f"Notatka klucza `{key}` wyczyszczona")


@bot.command()
async def info(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    v      = data[key]
    status = "Zbanowany" if v.get("banned") else ("Aktywny" if v.get("hwid") else "Oczekuje")
    dc     = v.get("debug_code") or "brak"
    await ctx.send(
        f"**Klucz:** `{key}`\n"
        f"**Status:** {status}\n"
        f"**HWID:** `{v.get('hwid') or 'brak'}`\n"
        f"**Kod debug:** `{dc}`\n"
        f"**Notatka:** {v.get('note') or 'brak'}"
    )


@bot.command(name="list")
async def list_cmd(ctx):
    data = load_licenses()
    if not data:
        return await ctx.send("Brak kluczy.")
    lines = []
    for k, v in data.items():
        status     = "Ban" if v.get("banned") else ("OK" if v.get("hwid") else "??")
        hwid_short = (v.get("hwid", "")[:8] + "...") if v.get("hwid") else "brak"
        dc         = v.get("debug_code", "") or "-"
        note_s     = f" | {v.get('note','')[:20]}" if v.get("note") else ""
        lines.append(f"[{status}] `{k}` HWID:`{hwid_short}` Debug:`{dc}`{note_s}")
    await ctx.send(f"**Klucze ({len(data)}):**\n" + "\n".join(lines))


@bot.command()
async def debugcode(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    code = data[key].get("debug_code", "")
    if code:
        await ctx.send(f"Kod debug klucza `{key}`: `{code}`")
    else:
        await ctx.send(
            f"Klucz `{key}` nie ma jeszcze kodu debug — uruchom makro przynajmniej raz."
        )


@bot.command()
async def delete(ctx, key):
    data = load_licenses()
    if key not in data:
        return await ctx.send("Nie znaleziono klucza")
    del data[key]
    save_licenses(data)
    log_activity("DELETE", f"Klucz {key} usuniety przez {ctx.author}")
    await ctx.send(f"Klucz `{key}` usuniety")


# ── Webhook auto-handler ──────────────────────────────────────────

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    # Tylko wiadomosci od innych botow (webhooki z makra)
    if not message.author.bot or message.author == bot.user:
        return

    parsed = parse_webhook_message(message.content)
    key   = parsed.get('key')
    hwid  = parsed.get('hwid')
    dc    = parsed.get('debug_code')
    mtype = parsed.get('type')

    if not key or mtype != 'activation':
        return

    data = load_licenses()

    if key not in data:
        await message.channel.send(
            f"Nieznany klucz: `{key}` — nie istnieje w bazie."
        )
        return

    changed = False
    notes   = []

    # Przypisz HWID jesli pole jest puste
    if hwid and not data[key].get('hwid'):
        data[key]['hwid'] = hwid
        log_activity("AUTO-ASSIGN", f"HWID {hwid[:12]}... => {key}")
        notes.append(f"HWID przypisany: `{hwid[:20]}...`")
        changed = True
    elif hwid:
        notes.append("HWID juz przypisany (bez zmian)")

    # Zapisz debug_code tylko jesli pole jest puste (pierwszy raz, nie nadpisuje)
    if dc and not data[key].get('debug_code'):
        data[key]['debug_code'] = dc
        log_activity("DEBUG-CODE", f"Kod debug {key}: {dc}")
        notes.append(f"Kod debug zapisany: `{dc}`")
        changed = True

    if changed:
        save_licenses(data)
        print(f"[AUTO] {key}: {', '.join(notes)}")


# ── Web API ───────────────────────────────────────────────────────

async def handle_root(request):
    try:
        with open("templates/panel.html", "r") as f:
            return web.Response(text=f.read(), content_type="text/html")
    except Exception as e:
        return web.Response(text=f"Error: {e}", status=500)


async def handle_api_licenses(request):
    data = load_licenses()
    return web.json_response([
        {
            "key":        k,
            "hwid":       v.get("hwid", ""),
            "banned":     v.get("banned", False),
            "note":       v.get("note", ""),
            "debug_code": v.get("debug_code", ""),
            "active":     bool(v.get("hwid")) and not v.get("banned", False),
        }
        for k, v in data.items()
    ])


async def handle_api_log(request):
    return web.json_response(activity_log)


async def handle_api_stats(request):
    data    = load_licenses()
    total   = len(data)
    active  = sum(1 for v in data.values() if v.get("hwid") and not v.get("banned"))
    pending = sum(1 for v in data.values() if not v.get("hwid") and not v.get("banned"))
    banned  = sum(1 for v in data.values() if v.get("banned"))
    return web.json_response({"total": total, "active": active, "pending": pending, "banned": banned})


async def handle_api_generate(request):
    data = load_licenses()
    key  = generate_key()
    data[key] = {"hwid": "", "banned": False, "note": "", "debug_code": ""}
    save_licenses(data)
    log_activity("GENERATE", f"Klucz {key} wygenerowany z panelu")
    return web.json_response({"key": key})


async def handle_api_action(request):
    try:
        body   = await request.json()
        action = body.get("action")
        key    = body.get("key")
        data   = load_licenses()

        if key not in data:
            return web.json_response({"error": "Klucz nie istnieje"}, status=404)

        if action == "ban":
            data[key]["banned"] = True
            log_activity("BAN", f"Klucz {key} zbanowany z panelu")
        elif action == "unban":
            data[key]["banned"] = False
            log_activity("UNBAN", f"Klucz {key} odbanowany z panelu")
        elif action == "reset":
            data[key]["hwid"] = ""
            log_activity("RESET", f"HWID klucza {key} zresetowany z panelu")
        elif action == "delete":
            del data[key]
            log_activity("DELETE", f"Klucz {key} usuniety z panelu")
        elif action == "note":
            data[key]["note"] = body.get("note", "")
            log_activity("NOTE", f"Notatka klucza {key}: {body.get('note','')[:40]}")
        elif action == "clear_debug":
            data[key]["debug_code"] = ""
            log_activity("DEBUG-CLEAR", f"Kod debug klucza {key} wyczyszczony")
        else:
            return web.json_response({"error": "Nieznana akcja"}, status=400)

        save_licenses(data)
        return web.json_response({"ok": True})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


async def handle_ws(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws_clients.add(ws)
    try:
        async for _ in ws:
            pass
    finally:
        ws_clients.discard(ws)
    return ws


async def start_webserver():
    app = web.Application()
    app.router.add_get("/",             handle_root)
    app.router.add_get("/ws",           handle_ws)
    app.router.add_get("/api/licenses", handle_api_licenses)
    app.router.add_get("/api/log",      handle_api_log)
    app.router.add_get("/api/stats",    handle_api_stats)
    app.router.add_get("/api/generate", handle_api_generate)
    app.router.add_post("/api/action",  handle_api_action)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 5000)
    await site.start()
    print("Panel dostepny na porcie 5000")


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")
    await start_webserver()


bot.run(TOKEN)

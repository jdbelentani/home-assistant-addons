# -*- coding: utf-8 -*-
import os, json
from datetime import datetime, timedelta
import requests

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
HASS_URL = os.getenv('HASS_URL', 'http://127.0.0.1:8123')

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

BASE_DIR = "/config/ha_autonomous_agent"
LOGS = f"{BASE_DIR}/logs"
BKP = f"{BASE_DIR}/backups"
os.makedirs(LOGS, exist_ok=True)
os.makedirs(BKP, exist_ok=True)

def log(msg: str):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line)
    with open(f"{LOGS}/agent.log", "a", encoding="utf-8") as fh:
        fh.write(line + "\n")

def _get(p):
    try:
        r = requests.get(f"{HASS_URL}/api/{p}", headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"GET {p} falhou: {e}")
        return None

def _post(p, data=None):
    try:
        r = requests.post(f"{HASS_URL}/api/{p}", headers=HEADERS, json=data, timeout=10)
        r.raise_for_status()
        return r.json() if r.content else {}
    except Exception as e:
        log(f"POST {p} falhou: {e}")
        return None

def backup_entities():
    states = _get("states") or []
    path = f"{BKP}/entities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(states, fh, indent=2, ensure_ascii=False)
    log(f"Backup salvo: {path}")

def diagnose():
    devices = _get("devices") or []
    states = _get("states") or []
    entries = _get("config/config_entries") or []
    autos = [s for s in states if s.get("entity_id","").startswith("automation.")]
    log(f"Dispositivos: {len(devices)} | Entidades: {len(states)} | Automações: {len(autos)} | Integrações: {len(entries)}")
    return autos, entries, states

def fix_issues(autos, entries):
    turned_off = 0
    for a in autos:
        if a.get("state") != "on":
            if _post("services/automation/turn_off", {"entity_id": a["entity_id"]}) is not None:
                turned_off += 1
    log(f"Automações desativadas (problemáticas): {turned_off}")

    reloaded = 0
    for e in entries:
        if e.get("state") != "loaded":
            if _post(f"config/config_entries/entry/{e.get('entry_id')}/reload") is not None:
                reloaded += 1
    log(f"Integrações recarregadas: {reloaded}")

def optimize(states):
    suggestions = 0
    for s in states:
        attrs = s.get("attributes", {})
        if isinstance(attrs.get("scan_interval"), int) and attrs["scan_interval"] < 10:
            log(f"Sugerir aumentar scan_interval: {s['entity_id']} -> {attrs['scan_interval']}s")
            suggestions += 1
    log(f"Sugestões de performance: {suggestions}")

def ui_hints():
    log("Sugestões Lovelace: tema escuro, ícones personalizados, mini-graph-card e mushroom-cards por cômodo.")

def report():
    p = f"{LOGS}/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("Agente autônomo executado. Consulte agent.log para detalhes.\n")
    log(f"Relatório: {p}")

def main():
    if not ACCESS_TOKEN:
        log("Falta ACCESS_TOKEN (Options › access_token). Abortando.")
        return
    os.makedirs(BASE_DIR, exist_ok=True)
    log("=== Início do Agente Autônomo ===")
    backup_entities()
    autos, entries, states = diagnose()
    fix_issues(autos, entries)
    optimize(states)
    ui_hints()
    report()
    log("=== Fim do Agente ===")

if __name__ == "__main__":
    main()

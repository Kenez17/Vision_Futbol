import requests
import time
from config import N8N_WEBHOOK_URL, EVENT_COOLDOWNS

_last_event_time = {}

def send_event(event_type, equipo_origen="local", extra_info=None):
    """Envía evento al webhook de n8n con control de cooldown."""
    now = time.time()
    last = _last_event_time.get(event_type, 0)
    cooldown = EVENT_COOLDOWNS.get(event_type, 3)
    if now - last < cooldown:
        print(f"[Cooldown] Evento '{event_type}' ignorado (último hace {now-last:.1f}s)")
        return False

    payload = {
        "evento": event_type,
        "modo": "structured",
        "equipo_origen": equipo_origen,
        "minuto": "",   # opcional, se puede calcular
        "marcador": "", # opcional
        "jugador": ""   # opcional
    }
    if extra_info:
        payload["detalle"] = extra_info

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[OK] Evento '{event_type}' enviado a n8n")
            _last_event_time[event_type] = now
            return True
        else:
            print(f"[Error] HTTP {response.status_code}")
    except Exception as e:
        print(f"[Error] No se pudo enviar evento: {e}")
    return False
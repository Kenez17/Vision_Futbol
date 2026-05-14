# 🧠 Prototipo: Detección automática de eventos de fútbol con visión por computador

Este sistema es un **prototipo experimental** que analiza video (webcam o archivo) en tiempo real, detecta posibles goles usando **YOLOv8** y envía eventos a un webhook de **n8n** para activar un narrador deportivo automático (OpenAI + ElevenLabs).

Fue desarrollado como extensión de un sistema existente de narración manual, buscando reducir la dependencia humana en un 80-90%.

---

## 🎯 Estado actual del prototipo

✅ **Funciona**:  
- Captura video (local o webcam)  
- Detecta balón con YOLOv8  
- Aplica heurística simple: si el balón entra en los márgenes laterales (5% del borde), dispara evento `"gol"`  
- Envía el evento al webhook de n8n correctamente  
- n8n recibe el evento y procesa el flujo completo (OpenAI + ElevenLabs)

❌ **Problema conocido (no resuelto)**:  
- El **audio no se reproduce en la UI HTML** cuando el evento es enviado desde Python.  
- La misma UI sí reproduce el audio cuando se usa el botón de prueba rápida.  
- Se sospecha que el payload enviado por Python puede faltar campos (tono, longitud, fidelidad) o que el navegador bloquea el autoplay para eventos automáticos.

---

## 📁 Estructura del proyecto

Vision_Futbol/
├── main.py # Bucle principal, captura de video, lógica de eventos
├── detector.py # Clase SoccerEventDetector (YOLO + heurísticas)
├── webhook_client.py # Envío de eventos a n8n con cooldown
├── config.py # Parámetros ajustables (webhook, márgenes, cooldown)
├── utils.py # (vacío o utilidades auxiliares)
├── requirements.txt # Dependencias Python
└── README.md # Este archivo


---

## 🧪 Requisitos

- Python 3.8+
- Dependencias (instalar con `pip install -r requirements.txt`):

opencv-python
ultralytics
requests
numpy

- **Conexión activa** al webhook de n8n (URL configurable en `config.py`)
- Archivo de video o webcam

---

## ⚙️ Configuración

Edita `config.py` para ajustar:

```python
WEBCAM_ID = 0                         # 0 para webcam, o ruta a video
N8N_WEBHOOK_URL = "https://tu-webhook-n8n.com/webhook/narrate-ai"
GOAL_LEFT_MARGIN = 0.05               # 5% desde la izquierda
GOAL_RIGHT_MARGIN = 0.95              # 5% desde la derecha
EVENT_COOLDOWNS = {"gol": 5}          # segundos entre eventos del mismo tipo

Importante: La URL del webhook debe ser la misma que usa la UI HTML del sistema de narración.

python main.py

Se abrirá una ventana mostrando el video.

Cuando el balón cruce los márgenes definidos, se dibujará un rectángulo rojo y se enviará el evento "gol".

En la consola se verá [OK] Evento 'gol' enviado a n8n.


🐛 Problema de audio (por resolver)

Síntoma
La UI HTML (panel narrador) no reproduce el audio cuando el evento viene de este script.

La misma UI funciona correctamente con el botón de prueba rápida.

Posibles causas
Payload incompleto – El script solo envía evento, modo, equipo_origen. La UI envía además tono, longitud, fidelidad. n8n podría necesitarlos para generar un prompt válido.

Política de autoplay del navegador – El navegador bloquea la reproducción automática si no hubo interacción previa del usuario con la UI. La prueba rápida sí tiene clic, el evento automático no.

Respuesta no es audio – n8n podría estar devolviendo un JSON de error en lugar de MP3.

REVISAR LA CARPETA "SISTEMA NARRATIVO BASE" AHI ESTA EL JSON USADO EN n8n Y ES TOTALMENTE FUNCIONAL PARA COMPARAR COMO RECIBE LOS EVENTOS Y ADAPTAR EL EVENTO QUE SE ENVIA DESDE PYTHON POR VISION DE COMPUTADOR 

Próximos pasos sugeridos
Modificar webhook_client.py para incluir tono, longitud, fidelidad en el payload.

Agregar logs de depuración para inspeccionar la respuesta del webhook (tipo de contenido, primeros bytes).

Simular en Python el mismo payload que envía la UI (capturado con DevTools) y verificar si el audio se reproduce.

📌 Nota para asistentes de IA (como Leo AI)
Si estás leyendo este repositorio para ayudar a depurar, presta atención especial a:

El archivo webhook_client.py – la función send_event no envía tono, longitud, fidelidad.

Comparar con el payload que envía la UI (se puede ver en la pestaña Network de las herramientas de desarrollador).

El archivo config.py – asegurar que la URL del webhook es correcta y accesible.

La posibilidad de un error de CORS o de tipo MIME en la respuesta de n8n.

🧭 Siguientes fases (planeadas)
Mejorar detección (tracking de balón, área de gol configurable)

Añadir detección de córner y penalti

Reducir falsos positivos

Integración final con la UI y solución del audio




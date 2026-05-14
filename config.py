# Configuración del prototipo
WEBCAM_ID = r"C:\Users\Kevin Martínez\Desktop\Vision_Futbol\Recursos\video_prueba.mp4"   # Ruta a tu video de prueba
PROCESS_EVERY_N_FRAMES = 6        # Procesar 1 de cada 6 frames (aprox 5 fps si la fuente va a 30)
CONFIDENCE_THRESHOLD = 0.5        # Mínima confianza para detecciones
GOAL_AREA_MARGIN = 50             # px desde los bordes para considerar "área de gol"
COOLDOWN_SECONDS = 5              # Tiempo entre eventos del mismo tipo
N8N_WEBHOOK_URL = "https://asyndetic-brittaney-unloyally.ngrok-free.dev/webhook/narrate-ai"  # Tu webhook real
EVENT_COOLDOWNS = {               # Cooldown por tipo de evento (en segundos)
    "posible_gol": 5,
    "posible_corner": 5,
}
# Coordenadas del área de gol (se calibra manualmente)
# Por ahora usaremos márgenes izquierdo/derecho del frame
GOAL_LEFT_MARGIN = 0.05           # 5% desde la izquierda
GOAL_RIGHT_MARGIN = 0.95          # 95% desde la izquierda (5% desde derecha)
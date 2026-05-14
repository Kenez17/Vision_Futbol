import cv2
import time
from detector import SoccerEventDetector
from webhook_client import send_event
from config import WEBCAM_ID, PROCESS_EVERY_N_FRAMES

def main():
    # Inicializar captura de video
    cap = cv2.VideoCapture(WEBCAM_ID)
    if not cap.isOpened():
        print("Error: No se pudo abrir la fuente de video.")
        return

    detector = SoccerEventDetector()
    frame_count = 0
    last_event_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fin del video o error de captura.")
            break

        frame_count += 1
        # Procesar solo cada N frames
        if frame_count % PROCESS_EVERY_N_FRAMES != 0:
            # Mostrar frame sin procesar (opcional)
            cv2.imshow('Detección de Eventos', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # Detectar objetos
        detections = detector.detect_frame(frame)
        # Heurística: posible gol
        goal_possible, ball = detector.detect_possible_goal(detections, frame.shape)
        if goal_possible:
            # Dibujar círculo rojo alrededor del balón para feedback visual
            x1, y1, x2, y2 = ball['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, "POSIBLE GOL", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            # Enviar evento (con cooldown)
            send_event("Gol", equipo_origen="local")  # Aquí puedes detectar qué equipo ataca
        else:
            # También podrías dibujar el balón en verde si está fuera del área
            if ball:
                x1, y1, x2, y2 = ball['bbox']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Mostrar frame con anotaciones
        cv2.imshow('Detección de Eventos', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
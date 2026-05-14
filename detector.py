import cv2
import numpy as np
from ultralytics import YOLO
from config import CONFIDENCE_THRESHOLD, GOAL_LEFT_MARGIN, GOAL_RIGHT_MARGIN

class SoccerEventDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)  # Carga modelo preentrenado
        # Clases COCO que nos interesan: 0=persona, 32=balón deportivo (sports ball)
        self.ball_class_id = 32
        self.person_class_id = 0

    def detect_frame(self, frame):
        """Ejecuta YOLO sobre un frame y retorna detecciones filtradas."""
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if conf < CONFIDENCE_THRESHOLD:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            detections.append({
                'class': cls,
                'class_name': self.model.names[cls],
                'confidence': conf,
                'bbox': (x1, y1, x2, y2)
            })
        return detections

    def is_ball_in_goal_area(self, ball_bbox, frame_shape):
        """Determina si el balón está cerca del área de gol (izquierda o derecha)."""
        h, w = frame_shape[:2]
        x_center = (ball_bbox[0] + ball_bbox[2]) / 2
        left_limit = w * GOAL_LEFT_MARGIN
        right_limit = w * GOAL_RIGHT_MARGIN
        return x_center < left_limit or x_center > right_limit

    def detect_possible_goal(self, detections, frame_shape):
        """Heurística: hay balón Y está en área de gol."""
        balls = [d for d in detections if d['class'] == self.ball_class_id]
        if not balls:
            return False, None
        ball = balls[0]  # tomamos el de mayor confianza (ya ordenados por YOLO)
        in_area = self.is_ball_in_goal_area(ball['bbox'], frame_shape)
        return in_area, ball

    # Puedes añadir más heurísticas: detección de multitud (cambio de intensidad), etc.
import os
import cv2
import json
import numpy as np

from ultralytics import YOLO
from config import UMBRAL_CONF, FRAMES_SKIP_DEFAULT, FRAMES_EXTRA_POST_DETECTION, YOLO_MODEL_NAME, OUTPUT_DIR

def yolo_video_detector(objetos_interes, roi_mask_file_path, video_path):
    model = YOLO(YOLO_MODEL_NAME)
    mask = np.load(roi_mask_file_path)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps // 1.1) if fps > 0 else FRAMES_SKIP_DEFAULT
    print(f"[YOLO]\t\tFPS detectado: {fps:.2f} -> Saltando {frame_skip} frames entre análisis")

    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    frame_id = 0
    saved_count = 0
    ultimo_segundo_guardado = -1
    skip_counter = 0
    post_detection_frames = 0

    while cap.isOpened():
        detected_objects = []
        ret, frame = cap.read()
        if not ret:
            break
        frame_id += 1

        if skip_counter > 0:
            skip_counter -= 1
            continue

        results = model.predict(frame, verbose=False)[0]
        mostrar_frame = False

        for box in results.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label not in objetos_interes:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            if mask[cy, cx] == 255 and float(box.conf[0]) > UMBRAL_CONF:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {box.conf[0]:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                mostrar_frame = True
                detected_objects.append({
                    "label": label,
                    "confidence": float(box.conf[0]),
                    "bbox": [x1, y1, x2, y2],
                    "center": [cx, cy]
                })

        cv2.drawContours(frame, contornos, -1, (0, 0, 255), 2)

        if mostrar_frame:
            ms = cap.get(cv2.CAP_PROP_POS_MSEC)
            minutos = int(ms // 60000)
            segundos = int((ms % 60000) // 1000)

            if segundos != ultimo_segundo_guardado:
                ultimo_segundo_guardado = segundos
                output_filename = f"frame_{minutos:02d}m_{segundos:02d}s_{frame_id:06d}.jpg"
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                cv2.imwrite(output_path, frame)
                saved_count += 1
                # print(f"Guardado frame {frame_id} ({minutos}m{segundos}s): {output_path}")

                if detected_objects:
                    metadata = {
                        "frame_id": frame_id,
                        "time": f"{minutos:02d}:{segundos:02d}",
                        "objects": detected_objects
                    }

                    json_path = output_path.replace(".jpg", ".json")
                    with open(json_path, "w") as f:
                        json.dump(metadata, f, indent=2)

            post_detection_frames = FRAMES_EXTRA_POST_DETECTION
        else:
            if post_detection_frames > 0:
                post_detection_frames -= 1
                skip_counter = 0
            else:
                skip_counter = frame_skip

    cap.release()
    print(f"[YOLO]\t\tGuardados {saved_count} frames con detecciones dentro del ROI.")
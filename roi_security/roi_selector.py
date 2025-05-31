import cv2
import numpy as np

def roi_selector_initial_frame(video_path, roi_mask_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError("No se pudo leer el primer frame del video.")
    roi_points = []

    def draw_roi(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            roi_points.append((x, y))
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

    print("[ROI]\t\tHaz clic en el video para dibujar el polígono del ROI. Pulsa 'q' para finalizar.")
    cv2.namedWindow("Selecciona ROI")
    cv2.setMouseCallback("Selecciona ROI", draw_roi)

    while True:
        temp_frame = frame.copy()
        if len(roi_points) > 1:
            cv2.polylines(temp_frame, [np.array(roi_points)], isClosed=True, color=(0, 255, 0), thickness=2)

        cv2.imshow("Selecciona ROI", temp_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    if len(roi_points) >= 3:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(roi_points)], 255)
        np.save(roi_mask_path.replace(".npy",""), mask)
        # print(f"Máscara ROI guardada como {roi_mask_path}")
    else:
        print("ROI no válido: se necesitan al menos 3 puntos.")
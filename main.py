import os
import shutil
from config import OUTPUT_DIR, ROI_BASE_PATH, VIDEO_BASE_PATH

from roi_selector import roi_selector_initial_frame
from detector import yolo_video_detector
from agent_analyzer import gemini_api_llm, generar_reporte_desde_jsones
from twilio_whatsapp_conection import whatsapp_conection
from datetime import datetime

def main():

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(ROI_BASE_PATH):
        shutil.rmtree(ROI_BASE_PATH)
    os.makedirs(ROI_BASE_PATH, exist_ok=True)


    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    video_name = "video1.mp4"
    video_file_path = os.path.join(VIDEO_BASE_PATH,video_name)
    roi_mask_file_path = os.path.join(ROI_BASE_PATH,f"roi_mask_{fecha_actual}.npy")
    roi_selector_initial_frame(video_file_path, roi_mask_file_path)

    objetos_interes = ["person", "dog", "cat", "car", "bus", "truck", "motorcycle","bicycle"]
    yolo_video_detector(objetos_interes, roi_mask_file_path, video_file_path)

    reporte_txt = generar_reporte_desde_jsones()

    prompt = f"""
    Eres un analista de seguridad y has recibido los siguientes eventos de detección generados por un sistema de visión por computador.
    Reporte generado el {fecha_actual}.
    {reporte_txt}
    Redacta un informe de seguridad breve, profesional y orientado al cliente. El informe debe:
    - Resumir la actividad detectada, destacando la hora y frecuencia de los eventos.
    - Aclarar que varias detecciones pueden corresponder a la misma persona.
    - Identificar posibles patrones o anomalías (por ejemplo, movimientos repetitivos en horarios inusuales).
    - Señalar riesgos potenciales y si se recomienda tomar alguna medida.
    Evita tecnicismos innecesarios y enfócate en comunicar de forma clara y profesional.
    """
    # print(reporte_txt)
    respuesta_modelo = gemini_api_llm(prompt)
    whatsapp_conection(respuesta_modelo)


if __name__ == "__main__":
    main()
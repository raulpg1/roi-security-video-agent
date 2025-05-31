import os
import json
from collections import defaultdict
import google.generativeai as genai
from config import MODEL_NAME, GOOGLE_API_KEY, OUTPUT_DIR

def generar_reporte_desde_jsones():
    resumen = defaultdict(int)
    eventos = []

    archivos = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json")])

    for archivo in archivos:
        ruta = os.path.join(OUTPUT_DIR, archivo)
        with open(ruta, "r") as f:
            data = json.load(f)
            time = data.get("time", "desconocido")
            for obj in data.get("objects", []):
                resumen[obj["label"]] += 1
                eventos.append(f"{obj['label']} detectado a las {time}")

    # Crear resumen en lenguaje natural
    if not eventos:
        return "No se han detectado eventos relevantes en el período analizado."

    resumen_texto = "🛡️ *Reporte de seguridad:*\n\n"
    for clase, cantidad in resumen.items():
        resumen_texto += f"- {cantidad} detección(es) de *{clase}*\n"

    resumen_texto += "\n🕒 *Eventos detectados:*\n"
    resumen_texto += "\n".join(f"- {e}" for e in eventos[-5:])  # últimos 5 eventos

    return resumen_texto

def gemini_api_llm(user_prompt: str, retries: int = 3) -> dict | None:
    """
    Sends a prompt to the Gemini API and returns the parsed JSON response.

    Args:
        user_prompt (str): Prompt to send to Gemini.
        retries (int): Number of retry attempts on failure.

    Returns:
        dict | None: Parsed response or None on failure.
    """

    genai.configure(api_key=GOOGLE_API_KEY)
    print("[GEMINI]\tGenerando el reporte en base a las detecciones.")
    try:
        model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        print(f"[ERROR] Error al cargar el modelo '{MODEL_NAME}': {e}")
        return None

    try:
        response = model.generate_content(user_prompt)
        content = response.text
        return content
    except Exception as e:
        print(f"[ERROR] Fallo al generar/parsing respuesta: {e}")
        if retries > 0:
            print("[INFO] Reintentando...")
            return gemini_api_llm(user_prompt, retries - 1)
        return None
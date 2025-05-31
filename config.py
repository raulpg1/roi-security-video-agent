from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv(".env")

# Paths
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./detections")
ROI_BASE_PATH = os.getenv("ROI_BASE_PATH", "./roi_masks")
VIDEO_BASE_PATH = os.getenv("VIDEO_BASE_PATH", "./videos/")
YOLO_MODEL_NAME = os.getenv("YOLO_MODEL_NAME", "..weights/yolov8n.pt")

# Parámetros de detección
UMBRAL_CONF = float(os.getenv("UMBRAL_CONF", 0.4))
FRAMES_SKIP_DEFAULT = int(os.getenv("FRAMES_SKIP_DEFAULT", 5))
FRAMES_EXTRA_POST_DETECTION = int(os.getenv("FRAMES_EXTRA_POST_DETECTION", 0))

# Modelo LLM
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TWILIO_DESTINATION_NUMBER = os.getenv("TWILIO_DESTINATION_NUMBER")
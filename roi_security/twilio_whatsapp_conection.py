from twilio.rest import Client
from config import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, TWILIO_DESTINATION_NUMBER

def whatsapp_conection(respuesta_modelo):
    account_sid = TWILIO_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=TWILIO_FROM_NUMBER,
        to=TWILIO_DESTINATION_NUMBER,
        body=respuesta_modelo[:1599]
    )

    print("[twilio]\t\tSe ha enviado el reporte vía whatsapp.")
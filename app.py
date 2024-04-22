import base64
from PIL import Image
from io import BytesIO
import easyocr
import numpy as np

def base64_to_text(base64_image):
    # Decodificar la imagen base64
    image_data = base64.b64decode(base64_image)

    # Crear una imagen desde los datos decodificados
    img = Image.open(BytesIO(image_data))

    # Convertir la imagen a un array numpy
    img_np = np.array(img)

    # Utilizar EasyOCR para extraer el texto de la imagen
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_np)

    # Concatenar el texto extraído
    text = ' '.join([res[1] for res in result])

    return text

# Leer la imagen y convertirla a base64
with open("1.PNG", "rb") as image_file:
    # Leer los datos de la imagen
    encoded_string = base64.b64encode(image_file.read())

    # Convertir los datos binarios a una cadena ASCII
    base64_image = encoded_string.decode('utf-8')

# Ejecutar la función base64_to_text con la imagen en base64
texto = base64_to_text(base64_image)

import re
from datetime import datetime

def extract_ocr_data(ocr_text):
    # Extraer el número de cuenta del remitente
    sender_account_number = re.search(r"From Account \*\*\*(\d+)", ocr_text).group(1)

    # Extraer el nombre del banco del destinatario
    recipient_bank_name = re.search(r"Recipients Bank (.+)", ocr_text).group(1)

    # Extraer el número de cuenta del destinatario
    recipient_account_number = re.search(r"Recipients Account (\d+)", ocr_text).group(1)

    # Extraer el nombre del destinatario
    recipient_name = re.search(r"Recipients Name (.+)", ocr_text).group(1)

    # Extraer el monto
    amount = re.search(r"Amount RM ([\d,]+\.\d{2})", ocr_text).group(1)

    # Extraer la referencia del destinatario
    recipient_reference = re.search(r"Recipients Reference (.+)", ocr_text).group(1)

    # Extraer la fecha y hora de la transacción
    transaction_datetime_str = re.search(r"Transaction Date Time (.+ AM|PM)", ocr_text).group(1)
    transaction_datetime = datetime.strptime(transaction_datetime_str, "%d %b %Y %I:%M.%S %p")
    transaction_datetime_iso = transaction_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Extraer el número de referencia de DuitNow
    duitnow_reference_number = re.search(r"DultNow Reference Number (\d+)", ocr_text).group(1)

    # Crear el JSON
    ocr_json = {
        "SenderAccountNumber": sender_account_number,
        "RecipientBankName": recipient_bank_name,
        "RecipientAccountNumber": recipient_account_number,
        "RecipientName": recipient_name,
        "Amount": amount,
        "RecipientReference": recipient_reference,
        "TransactionDateTime": transaction_datetime_iso,
        "DuitNowReferenceNumber": duitnow_reference_number
    }

    return ocr_json

# Texto OCR proporcionado

ocr_json = extract_ocr_data(texto.replace('"',"").replace("'","").replace("'",""))
print(ocr_json)

import json
from colorama import init, Fore, Style

pretty_json = json.dumps(ocr_json, indent=4)

# Imprimir el JSON con colores
print(Fore.GREEN + pretty_json)
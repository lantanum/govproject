import qrcode
from io import BytesIO
import base64
import json

def generate_qr_code(data):
    qr = qrcode.make(json.dumps(data))
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode()

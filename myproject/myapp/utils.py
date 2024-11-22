import qrcode
import io
import base64
from datetime import datetime, timedelta

def generate_qr_code(data, expiration_minutes=3):
    """
    Генерирует QR-код с уникальными данными и временем действия.
    """
    expiration_time = (datetime.now() + timedelta(minutes=expiration_minutes)).strftime('%Y-%m-%d %H:%M:%S')
    qr_data = f"{data}|{expiration_time}"  # Логин и время действия

    # Создание QR-кода
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Конвертация изображения в base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return img_base64, expiration_time  # Возвращаем срок действия QR-кода

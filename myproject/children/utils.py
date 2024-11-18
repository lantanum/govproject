import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(child):
    qr_data = f"IIN: {child.iin}, Name: {child.full_name}"
    qr_img = qrcode.make(qr_data)
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    filename = f'qr_code_{child.iin}.png'
    child.qr_code.save(filename, File(buffer), save=False)

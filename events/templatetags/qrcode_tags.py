# yourapp/templatetags/qrcode_tags.py

from django import template
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def qr_code_image(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an in-memory stream to save the image
    stream = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(stream, "PNG")
    qr_code_image = stream.getvalue()

    return mark_safe(qr_code_image.decode('utf-8'))

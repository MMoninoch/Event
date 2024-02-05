import base64
from django import template

register = template.Library()

@register.filter
def base64_encode(value):
    try:
        # Convert the value to bytes if it's a string
        if isinstance(value, str):
            value = value.encode('utf-8')

        # Encode to base64
        encoded = base64.b64encode(value).decode('utf-8')
        return encoded
    except Exception as e:
        # Handle encoding errors if necessary
        return ''

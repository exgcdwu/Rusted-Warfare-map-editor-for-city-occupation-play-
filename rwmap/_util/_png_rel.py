import base64
from io import BytesIO
from PIL import Image

def image_width(image_file:str)->int:
    with Image.open(image_file) as img:
        return img.width
    
def image_height(image_file:str)->int:
    with Image.open(image_file) as img:
        return img.height
    
def get_png_text(image:Image.Image)->str:
    byte_arr = BytesIO()
    image.save(byte_arr, format = 'PNG')
    base64_str = base64.b64encode(byte_arr.getvalue()).decode('utf-8')
    return base64_str
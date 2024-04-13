from PIL import Image

def image_width(image_file:str)->int:
    with Image.open(image_file) as img:
        return img.width
    
def image_height(image_file:str)->int:
    with Image.open(image_file) as img:
        return img.height
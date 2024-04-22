from wand.image import Image
from src.config import config
import os


class Converter:
    def __init__(self, image_in: str):
        self.image_in = str(image_in)
        self.image_out: str = "output_" + str(image_in)
        self.image: Image = Image(filename=os.path.join(config.UPLOAD_DIR, self.image_in))
    
    def save(self) -> str:
        self.image.save(filename=os.path.join(config.UPLOAD_DIR, self.image_out))
        return self.image_out
    
    def resize(self, width, height):
        self.image.resize(width, height)
        return self.save()
    
    def crop(self, width, height):
        self.image.crop(width, height)
        return self.save()
    
    def rotate(self, degrees):
        self.image.rotate(degrees)
        return self.save()
    
    def brightness(self, value):
        self.image.modulate(brightness=value)
        return self.save()
    
    def contrast(self, value):
        self.image.modulate(contrast=value)
        return self.save()
    
    def edge(self, radius):
        self.image.edge(radius)
        return self.save()
    
    def convert(self, image_type):
        self.image.convert(image_type)
        return self.save()
    

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
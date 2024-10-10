from wand.image import Image
from src.config import config
import os


class Converter:
    def __init__(self, image_in: str):
        self.image_in = str(image_in)
        self.image_out: str = "o_" + str(image_in)
        self.image: Image = Image(filename=os.path.join(config.CONVERTED_DIR, self.image_in))
    
    def save(self) -> str:
        self.image.save(filename=os.path.join(config.CONVERTED_DIR, self.image_out))
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
        try:
            self.image = self.image.convert(image_type)
            self.image_out = self.image_out[:-5] + "." + str(image_type) # remove the last 5 characters to remove the extention like .png and add the new extension
            return self.save(), None
        except Exception as e:
            return "Failed to convert the image.", e
                
        
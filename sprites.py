import os
import pygame as pg
from PIL import Image
from graphics import Texture, Canvas, Transform

class Sprites:

    def __init__(self):

        self.spritesheets: dict = {}

        self.init_load()

    def init_load(self):

        # Load relevant spritesheets
        self.load_sprites(paths={
            r"_sprites\spritesheet1.png",
        })

    
    def load_sprites(self, paths:set):

        # Load spritesheet surfaces
        for path in paths:

            # Load spritesheet data
            name: str = os.path.basename(path).split(".")[0]
            texture: Texture = Sprites.load_image_as_texture(path=path)
            tilesize: tuple = Sprites.scan_spritesheet(path=path); 
            
            # Load sprites
            sprites: list = Sprites.split_spritesheet(spritesheet=texture, tilesize=tilesize)
            self.spritesheets[name]: list = sprites

    @staticmethod
    def scan_spritesheet(path:str):
        
        # Open file
        spritesheet: Image.Image = Image.open(fp=path).convert("RGB")
        size: tuple = spritesheet.size
        
        # Scan for red-pixel on x-axis (255,0,0) for width
        for x in range(size[0]):
            pixel_colour: tuple = spritesheet.getpixel(xy=(x,0))
            if pixel_colour == (255, 0, 0):
                break
        
        # Scan for blue-pixel on y-axis (0,0,255) for height
        for y in range(size[1]):
            pixel_colour: tuple = spritesheet.getpixel(xy=(x,y))
            if pixel_colour == (0, 0, 255):
                break

        spritesheet.close()

        return (x+1, y+1)
    
    @staticmethod
    def split_spritesheet(spritesheet:Texture, tilesize:tuple):
        
        sprites: list = []
                
        # Find num of iterations for sprite parsing
        x_num_tiles = spritesheet.size[0] // tilesize[0]
        y_num_tiles = spritesheet.size[1] // tilesize[1]
        
        # Sprite segmenter loop
        for y in range(y_num_tiles):
            for x in range(x_num_tiles):
 
                # Load sprite as pg surface
                texture: Texture = Sprites.load_blank_texture(size=tilesize)
                texture.blit(source=spritesheet, pos=(-x * tilesize[0], -y * tilesize[1]), area=(0, 0, tilesize[0], tilesize[1]))
                texture = Sprites.resize_surface(texture=texture, x_scale=4, y_scale=4)
                
                sprites.append(texture)

        return sprites

    @staticmethod
    def load_image_as_texture(path:str):
        
        # Load spritesheet as graphics.Texture
        return Texture.load(path=path)

    @staticmethod
    def load_blank_texture(size:tuple):
        return Texture.load_blank(size=size, channels=4)

    @staticmethod
    def resize_surface(texture:Texture, x_scale:int, y_scale:int):
        return Transform.scale(source=texture, size=(texture.size[0]*x_scale, texture.size[1]*y_scale))

    def garbage_cleanup(self):
        for sheet in self.spritesheets:
            for sprite in self.spritesheets[sheet]:
                sprite.release()




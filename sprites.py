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

    def garbage_cleanup(self):
        pass

    def load_sprites(self, paths:set):

        # Load spritesheet surfaces
        for path in paths:

            # Load spritesheet data
            name: str = os.path.basename(path).split(".")[0]
            surface: Surface = Sprites.load_image_as_surface(path=path)
            tilesize: tuple = Sprites.scan_spritesheet(path=path); 
            
            # Load sprites
            sprites: list = Sprites.split_spritesheet(spritesheet=surface, tilesize=tilesize)
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
    def split_spritesheet(spritesheet:pg.Surface, tilesize:tuple):
        
        sprites: list = []
                
        # Find num of iterations for sprite parsing
        spritesheet_size: tuple = spritesheet.get_size()
        x_num_tiles = spritesheet_size[0] // tilesize[0]
        y_num_tiles = spritesheet_size[1] // tilesize[1]
        
        # Sprite segmenter loop
        for y in range(y_num_tiles):
            for x in range(x_num_tiles):
 
                # Load sprite as pg surface
                surface: pg.Surface = pg.Surface(size=tilesize).convert_alpha()
                surface.blit(source=spritesheet, dest=(0,0), area=(x*tilesize[0], y*tilesize[1], x*x_num_tiles+tilesize[0], y*y_num_tiles+tilesize[1]))
                surface = Sprites.resize_surface(surface=surface, x_scale=4, y_scale=4)
                
                sprites.append(surface)

        return sprites

    @staticmethod
    def load_image_as_surface(path:str):
        # Load spritesheet as pg surface
        return pg.image.load(path).convert_alpha()

    @staticmethod
    def resize_surface(surface:pg.Surface, x_scale:int, y_scale:int):
        return pg.transform.scale(surface=surface, size=(surface.get_width() * x_scale, surface.get_height() * y_scale))






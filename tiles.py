from pygame   import Rect
from graphics import Texture

class Tile:
    def __init__(self, layer_id:int, tile_size:tuple, tile_pos:tuple, tile_textures:list, tile_rect:Rect, tile_properties:dict):
        
        self.layer_id:   int   = layer_id
        self.size:       tuple = tile_size
        self.pos:        tuple = tile_pos
        self.textures:   list  = tile_textures
        self.rect:       Rect  = tile_rect
        self.properties: dict  = tile_properties

        self.current_frame: int = 0

    def update(self):
        pass

    def draw(self):
        pass

    def draw_shader(self):
        pass

    def garbage_cleanup(self):
        pass

    def animate(self):
        pass

    def move(self):
        pass

    def get_frame(self):
        """Returns the current animated texture frame"""

        return self.textures[self.current_frame]



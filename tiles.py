from pygame   import Rect
from graphics import Texture

class Tile:
    def __init__(self, layer_id:int, size:tuple, pos:tuple, textures:list, rect:Rect, properties:dict):
        
        self.layer_id:   int   = layer_id
        self.size:       tuple = size
        self.pos:        tuple = pos
        self.textures:   list  = textures
        self.rect:       Rect  = rect
        self.properties: dict  = properties

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



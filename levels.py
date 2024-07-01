from pygame import Rect
from tiles  import Tile
from layers import TileLayer
from layers import EntityLayer
from layers import LightingLayer
from layers import CollisionLayer
from layers import BackgroundLayer


class Level:
    def __init__(self, WorldModule, SpriteModule, GraphicsModule, level_data:dict):
        
        self.WORLDMODULE    = WorldModule
        self.SPRITEMODULE   = SpriteModule
        self.GRAPHICSMODULE = GraphicsModule

        self.level_data: dict  = level_data     # .tmj (json) to python (dict)
        self.name:       str   = ""             # level displayname <string>
        self.size:       tuple = ()             # (width,height)
        self.tilesize:   tuple = ()             # (width,height)
        self.layers:     list  = []             # [layer1, layer2, layer3]      


    def init_load(self):
        self.load_information(data=self.level_data)
        self.load_tilelayers(data=self.level_data["layers"])
        # self.load_imagelayers()
    
    def load_information(self, data:dict):
        
        self.name     = ""
        self.size     = (data["width"], data["height"])
        self.tilesize = (data["tilewidth"], data["tileheight"])


    def load_tilelayers(self, data:list):
        
        layers: list = []
        for layer in layers:
            
            # Skip non-tilelayers
            if layer["type"] != "tilelayer": continue

            # Operations
            



    def load_imagelayers(self):
        pass

    def load_lightinglayers(self):
        pass

    def load_entitylayers(self):
        pass

    def colliderlayers(self):
        pass
from json import load
from graphics import Texture
from pygame import Rect

class World:
    def __init__(self):
        
        self.level_data: dict = {}
        self.current_level: Level = None
        
    def init_load(self):
        
        # Load level data
        self.load_data(
            paths={
                r"_levels\level_1.tmj"
            }
        )


    def load_data(self, paths:set):
        
        for path in paths:
            name: str; extension: str
            name, extension = path.split("\\")[-1].split(".")
            with open(file=path, mode="r") as f:
                data: dict = load(f)
                self.level_data[name] = data

    def load_level(self, level_name:str):
        
        data: dict = self.level_data[level_name]
        level: Level = Level(level_data=data)

        self.current_level = level


class Level:
    def __init__(self, level_data:dict):
        
        self.level_data: dict = level_data
        self.name: str   = ""
        self.size: tuple = ()
        self.tilesets:     list = []
        self.tilelayers:   list = []
        self.objectlayers: list = []
        

        self.backgrounds:   list = []
        self.shaders:       list = []
        self.tiles:         list = []
        self.entities:      list = []
        self.players:       list = []
        self.lights:        list = []

    @staticmethod
    def convert_bitmap_1d_to_2d(bitmap:list, size:tuple):
        
        if len(bitmap) != size[1] * size[0]:
            return "Invalid input dimensions"
        
        reshaped_array = []
        for i in range(0, len(bitmap), size[0]):
            row = bitmap[i:i+size[0]]
            reshaped_array.append(row)

        return reshaped_array


    def init_load(self):
        self.load_information()

    
    def load_information(self):
        
        data: dict  = self.level_data
        name: str   = ""
        size: tuple = ()
        tilelayers:   dict  = {}
        objectlayers: dict  = {}
        tilesets:     list  = []

        # Get size
        size = (data["width"], data["height"])

        # Load tilelayers
        for lay in data["layers"]:
            layertype: str    = lay["type"]
            layerid:   int    = lay["id"]
            layersize: tuple  = (lay["width"], lay["height"])
            bitmap:     dict  = lay["bitmap"] if layertype == "tilelayer" else {}
            objectmap:  dict  = lay["objects"] if layertype == "objectgroup" else {}

            
            # Load as tilelayer
            if layertype == "tilelayer":
                tilelayers[layerid] = {"size": layersize, "type": layertype, "bitmap": bitmap, "objectmap": objectmap}
            
            # Load as objectgroup
            elif layertype == "objectgroup":
                objectlayers[layerid] = {"size": layersize, "type": layertype, "bitmap": bitmap, "objectmap": objectmap}


        # Get tilesets
        for til in data["tilesets"]:
            firstgrid: int = til["firstgid"]
            source:    str = til["source"].split("/")[-1].split(".")[0]     # eg: "..\/_sprites\/spritesheet1.tsx" to "spritesheet1"   
            
            tilesets.append({"firstgrid": firstgrid, "source": source})


        # Assign information 
        self.name = name
        self.size = size
        self.tilesets     = tilesets
        self.tilelayers   = tilelayers
        self.objectlayers = objectlayers

    def load_tiles(self):

        # {"size": size, "type": _type, "bitmap": bitmap}
        tiles: list = []
        for lay in self.tilelayers:
            
            size:   tuple = lay["size"]
            bitmap: list  = lay["bitmap"]
            bitmap = Level.convert_bitmap_1d_to_2d(bitmap=bitmap, size=size)

            tile: Tile = Tile(

            )
            tiles.append(tile)

        # Assing
        self.tiles = tiles

    def load_backgrounds(self):
        pass

    def load_shaders(self):
        pass

    def load_entites(self):
        pass

    def load_players(self):
        pass

    def load_lights(self):
        pass


class Tile:
    def __init__(self, size:tuple, pos:tuple, textures:list, rect:Rect, properties:dict):
        
        self.size:       tuple = size
        self.pos:        tuple = pos
        self.textures:   list  = textures
        self.rect:       Rect  = rect
        self.properties: dict  = properties


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






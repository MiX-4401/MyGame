from json import load
from graphics import Texture
from pygame   import Rect
from sprites  import Sprites
from graphics import Graphics

class World:
    def __init__(self, SpriteModule:Sprites, GraphicsModule:Graphics):
        
        self.SPRITEMODULE:   Sprites  = SpriteModule
        self.GRAPHICSMODULE: Graphics = GraphicsModule
        self.level_data: dict = {}
        self.current_level: Level = None

        self.init_load()

        self.load_level(level_name="level_1")
        
    def init_load(self):
        
        # Load level data
        self.load_data(
            paths={
                r"_levels\level_1.tmj"
            }
        )


    def load_data(self, paths:set):
        """Gets all level data from paths argument (json to dictionary)"""

        for path in paths:
            name: str; extension: str
            name, extension = path.split("\\")[-1].split(".")
            with open(file=path, mode="r") as f:
                data: dict = load(f)
                self.level_data[name] = data

    def load_level(self, level_name:str):
        """Gets and loads level data into a class resource"""

        data: dict = self.level_data[level_name]
        level: Level = Level(
            WorldModule=self, 
            SpriteModule=self.SPRITEMODULE, 
            GraphicsModule=self.GRAPHICSMODULE,
            level_data=data
        )

        self.current_level = level


class Level:
    def __init__(self, WorldModule: World, SpriteModule: Sprites, GraphicsModule: Graphics, level_data:dict):
        
        self.WORLDMODULE:    World    = WorldModule
        self.SPRITEMODULE:   Sprites  = SpriteModule
        self.GRAPHICSMODULE: Graphics = GraphicsModule

        self.level_data: dict = level_data  # .tmj (json) to python (dict)
        self.name: str   = ""               # level displayname <string>
        self.size: tuple = ()               # (width,height)
        self.tilesize:     tuple = ()       # (width,height)
        self.tilesets:     dict  = {}       # {bitmapid: {'spritesheet': str 'textureindex': int}}
        self.tilelayers:   dict  = {}       # {'size': (width,height), 'type': layertype, 'bitmap': list}
        self.objectlayers: dict  = {}       # {'size': (width,height), 'type': layertype, 'objectmap': list}
        

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
        
        self.name     = ""
        self.size     = (data["width"], data["height"])
        self.tilesize = (data["tilewidth"], data["tileheight"])

        self.load_tilelayers()
        self.load_objectlayers()
        self.load_tilesets()

    def load_tilelayers(self):
        
        # Load tilelayers
        
        tilelayers: dict = {}
        for lay in self.level_data["layers"]:
            if lay["type"] != "tilelayer": continue

            layertype: str    = lay["type"]
            layerid:   int    = lay["id"]
            layersize: tuple  = (lay["width"], lay["height"])
            bitmap:     dict  = lay["bitmap"]

            bitmap = Level.convert_bitmap_1d_to_2d(bitmap=bitmap, size=size)
            tilelayers[layerid] = {"size": layersize, "type": layertype, "bitmap": bitmap}
            
        self.tilelayers = tilelayers

    def load_objectlayers(self):

        # Load objectlayers

        objectlayers: dict = {}
        for lay in self.level_data["layers"]:
            if lay["type"] != "objectgroup": continue

            layertype: str    = lay["type"]
            layerid:   int    = lay["id"]
            layersize: tuple  = (lay["width"], lay["height"])
            objectmap:  dict  = lay["objects"]

            objectlayers[layerid] = {"size": layersize, "type": layertype, "objectmap": objectmap}

        self.objectlayers = objectlayers

    def load_tilesets(self):
        
        # Get tilesets
        tilesets: dict = {}         
        for til in self.level_data["tilesets"]:
            firstgrid: int = til["firstgid"]
            source:    str = til["source"].split("/")[-1].split(".")[0]     # eg: "..\/_sprites\/spritesheet1.tsx" to "spritesheet1"   
            
            spritesheet: list = self.SPRITEMODULE.spritesheets[source]

            # Match the level bitmap tile id with a spritesheet texture index
            for textureindex,bitmapid in enumerate([e for e in range(firstgrid + len(spritesheet))][firstgrid::]):
                tilesets[bitmapid] = {
                    "spritesheet":  source,
                    "texture_index": textureindex
                }

    def load_tiles(self):

        # {"size": size, "type": _type, "bitmap": bitmap}
        tiles: list = []
        for layerid in self.tilelayers:

            bitmap: list = self.tilelayers[layerid]["bitmap"]

            for i,y in enumerate(bitmap):
                for ii,x in enumerate(bitmap):
                    
                    rect = Rect(
                        left=ii*self.tilesize[0],
                        top=i*self.tilesize[1],
                        width=self.tilesize[0],
                        height=self.tilesize[1]
                    ) 

                    tile: Tile = Tile(
                        size=self.tilesize,
                        pos=[ii*self.tilesize[0], i*self.tilesize[1]],
                        textures=self.SPRITEMODULE.return_tile_texture(spritesheet=self.tilesets[x]["spritesheet"], index=self.tilesets[x]["texture_index"]),
                        rect=rect if layerid == "1" else None,
                        properties={}
                    )
            tiles.append(tile)

        # Assign
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

    def load_graphics(self):
        for i in range(len(self.tilelayers)):
            self.GRAPHICSMODULE.register_canvas()



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






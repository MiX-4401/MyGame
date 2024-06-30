from pygame import Rect
from tiles  import Tile
# from layers import TileLayer, EntityLayer


class Level:
    def __init__(self, WorldModule, SpriteModule, GraphicsModule, level_data:dict):
        
        self.WORLDMODULE    = WorldModule
        self.SPRITEMODULE   = SpriteModule
        self.GRAPHICSMODULE = GraphicsModule

        self.level_data: dict = level_data  # .tmj (json) to python (dict)
        self.name: str   = ""               # level displayname <string>
        self.size: tuple = ()               # (width,height)
        self.tilesize:     tuple = ()       # (width,height)
        self.tilesets:     dict  = {}       # {bitmapid: {'spritesheet': str 'textureindex': int}}
        self.tilelayers:   dict  = {}       # {'size': (width,height), 'type': layertype, 'bitmap':    list, 'properties': [{prop: value}]}
        self.objectlayers: dict  = {}       # {'size': (width,height), 'type': layertype, 'objectmap': list, 'properties': [{prop: value}]}
        

        self.backgrounds:   list = []
        self.shaders:       list = []
        self.tiles:         dict = {}       # {layerid: [tile1, tile2, tile3]}
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
        self.load_tilelayers()
        self.load_objectlayers()
        self.load_tilesets()
        self.load_tiles()
        self.load_graphics()

    
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
            
            layertype:  str   = lay["type"]
            layerid:    int   = lay["id"]
            layersize:  tuple = (lay["width"], lay["height"])
            bitmap:     dict  = lay["data"]
            offset:     tuple = (lay["offsetx"]*self.SPRITEMODULE.scale_factor*-1, lay["offsety"]*self.SPRITEMODULE.scale_factor*-1) if "offsetx" in lay else (0, 0)
            properties: dict  = {prop["name"]: prop["value"] for prop in lay["properties"]}

            bitmap = Level.convert_bitmap_1d_to_2d(bitmap=bitmap, size=layersize)
            tilelayers[layerid] = {"size": layersize, "offset": offset, "type": layertype, "bitmap": bitmap, "properties": properties}
            
        self.tilelayers = tilelayers

    def load_objectlayers(self):

        # Load objectlayers

        objectlayers: dict = {}
        for lay in self.level_data["layers"]:
            if lay["type"] != "objectgroup": continue

            layertype: str    = lay["type"]
            layerid:   int    = lay["id"]
            objectmap:  dict  = lay["objects"]

            objectlayers[layerid] = {"type": layertype, "objectmap": objectmap}

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
        
        self.tilesets = tilesets

    def load_tiles(self):

        # {"size": size, "type": _type, "bitmap": bitmap}
        tiles: dict = {}
        for layerid in self.tilelayers:
            tiles[layerid]: list = []

            bitmap: list = self.tilelayers[layerid]["bitmap"]

            # FOR each tile appearing on the bitmap
            for i,y in enumerate(bitmap):
                for ii,x in enumerate(y):
                    
                    if x == 0: continue

                    # Create tile collider
                    rect = Rect(
                        ii*self.tilesize[0]*self.SPRITEMODULE.scale_factor,
                        i*self.tilesize[1]*self.SPRITEMODULE.scale_factor,
                        self.tilesize[0]*self.SPRITEMODULE.scale_factor,
                        self.tilesize[1]*self.SPRITEMODULE.scale_factor
                    ) 

                    # Create tile
                    tile: Tile = Tile(
                        layer_id=layerid,
                        size=self.tilesize,
                        pos=[ii*self.tilesize[0]*self.SPRITEMODULE.scale_factor, i*self.tilesize[1]*self.SPRITEMODULE.scale_factor],
                        textures=[self.SPRITEMODULE.return_tile_texture(spritesheet=self.tilesets[x]["spritesheet"], index=self.tilesets[x]["texture_index"])],
                        rect=rect if layerid == "1" else None,
                        properties={}
                    )

                    # Add tile to list
                    tiles[layerid].append(tile)

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
        graphics = self.GRAPHICSMODULE

        # Register canvases
        for lay in self.tilelayers:
            graphics.register_canvas(name=lay, size=graphics.canvases["main"].size, channels=4)

        # Draw tiles onto static canvases
        for layerid in self.tiles:
            
            # Get render target (canvas) & list of tiles
            canvas     = graphics.canvases[layerid]
            tiles      = self.tiles[layerid]
            properties = self.tilelayers[layerid]["properties"]

            # Skip non-static layers
            if properties["draw_static"] == False: continue

            # Blit tiles onto static-canvas
            for til in tiles:
                canvas.blit(
                    source=til.get_frame(), 
                    pos=til.pos
                )


    def update(self):
        pass

    def draw(self):

        graphics = self.GRAPHICSMODULE

        # Draw tiles onto non-static canvases
        for layerid in self.tiles:
            
            # Get render target (canvas) & list of tiles
            canvas     = graphics.canvases[layerid]
            tiles      = self.tiles[layerid]
            properties = self.tilelayers[layerid]["properties"]

            # Skip static layers
            if properties["draw_static"] == True: continue

            # Blit tiles onto canvas
            for til in tiles:
                canvas.blit(
                    source=til.get_frame(), 
                    pos=til.pos
                )
        
        # Draw canvases
        for canvasid in graphics.canvases:
            offset = self.tilelayers[canvasid]["offset"] if canvasid != "main" else (0,0) 
            graphics.draw(destination="main", source=canvasid, pos=offset)

    def garbage_cleanup(self):
        pass




from tiles  import Tile
from pygame import Rect



class TileLayer:
    tilesets: dict = {}

    def __init__(self, tile_size:tuple, layer_name:str, layer_id:int, layer_size:tuple, layer_offset:tuple, layer_bitmap:list, layer_properties:dict):
        self.name:       str   = layer_name
        self.id:         int   = layer_id,
        self.size:       tuple = layer_size
        self.offset:     tuple = layer_offset
        self.bitmap:     list  = layer_bitmap
        self.properties: dict  = layer_properties
        
        self.tilesize:  tuple = tile_size
        self.tiles:     list  = []

    def load_init(self):
        self.bitmap = Level.convert_bitmap_1d_to_2d(bitmap=self.bitmap, size=self.size)
        self.load_tiles()


    def load_tiles(self):
        """Loads tiles into self.tile variable"""

        tiles: list = [] 

        # FOR each tile appearing on the bitmap
        for i,y in enumerate(self.bitmap):
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
                    layer_id=self.id,
                    tile_size=self.tilesize,
                    tile_pos=[ii*self.tilesize[0]*self.SPRITEMODULE.scale_factor, i*self.tilesize[1]*self.SPRITEMODULE.scale_factor],
                    tile_textures=[self.SPRITEMODULE.return_tile_texture(spritesheet=TileLayer.tilesets[x]["spritesheet"], index=TileLayer.tilesets[x]["texture_index"])],
                    tile_rect=rect if layerid == "1" else None,
                    tile_properties={}
                )


                tiles.append(tile)
        self.tiles = tiles


    @staticmethod
    def convert_bitmap_1d_to_2d(bitmap:list, size:tuple):
        
        if len(bitmap) != size[1] * size[0]:
            return "Invalid input dimensions"
        
        reshaped_array = []
        for i in range(0, len(bitmap), size[0]):
            row = bitmap[i:i+size[0]]
            reshaped_array.append(row)

        return reshaped_array


class ImageLayer:
    def __init__(self, layer_name:str, layer_id:int, layer_image_path:str, layer_offset:tuple, layer_pallerax:tuple, layer_properties:dict):
        self.name:        str   = layer_name
        self.id:          int   = layer_id
        self.image_path:  str   = layer_image_path
        self.offset:      tuple = layer_offset
        self.pallerax:    tuple = layer_pallerax
        self.properties:  dict  = layer_properties


class EntityLayer:
    def __init__(self, layer_name:str, layer_id:int, layer_entities:list, layer_properties:dict):
        self.name:       str  = layer_name
        self.id:         int  = layer_id
        self.entities:   list = layer_entities
        self.properties: dict = layer_properties


class LightingLayer:
    def __init__(self, layer_name:str, layer_id:int, layer_lights:list, layer_properties:dict):
        self.name:       str  = layer_name
        self.id:         int  = layer_id
        self.lights:     list = layer_lights
        self.properties: dict = layer_properties


class CollisionLayer:
    def __init__(self):
        pass





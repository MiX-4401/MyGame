from pygame import Rect
from tiles  import Tile
from layers import TileLayer
from layers import ImageLayer
from layers import EntityLayer
from layers import LightingLayer
from layers import CollisionLayer


class Level:
    def __init__(self, WorldModule, SpriteModule, GraphicsModule, level_data:dict):
        
        self.WORLDMODULE    = WorldModule
        self.SPRITEMODULE   = SpriteModule
        self.GRAPHICSMODULE = GraphicsModule

        self.level_data: dict  = level_data     # .tmj (json) to python (dict)
        self.name:       str   = ""             # level displayname <string>
        self.size:       tuple = ()             # (width,height)
        self.tilesize:   tuple = ()             # (width,height)
        self.tilesets:   dict  = {}
        self.layers:     list  = []             # [layer1, layer2, layer3]      
    

    def init_load(self):
        self.load_information(data=self.level_data)
        self.load_tilelayers(data=self.level_data["layers"])
        self.load_imagelayers(data=self.level_data["layers"])
        self.load_entitylayers(data=self.level_data["layers"])
        self.load_lightinglayers(data=self.level_data["layers"])
    

    def load_information(self, data:dict):
        """Load basic level information"""

        self.name     = ""
        self.size     = (data["width"], data["height"])
        self.tilesize = (data["tilewidth"], data["tileheight"])


    def load_tilesets(self, data:dict):
        """Loads tilesets"""

        tilesets: dict = {}         
        for til in data["tilesets"]:
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


    def load_tilelayers(self, data:list):
        """Load a list of tilelayers in the level"""


        tile_layers: list = []
        for layer in data["layers"]:
            
            # Skip non-tilelayers
            if layer["type"] != "tilelayer": continue


            # Get tilelayer information
            layer_id:         int   = layer["id"]
            layer_name:       str   = layer["name"]
            layer_size:       tuple = (layer["width"], layer["height"])
            layer_offset:     tuple = (layer["offsetx"]*self.SPRITEMODULE.scale_factor*-1, layer["offsety"]*self.SPRITEMODULE.scale_factor*-1) if "offsetx" in layer else (0, 0)
            layer_bitmap:     list  = layer["bitmap"]
            layer_properties: dict  = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load tilelayer
            tilelayer: TileLayer = TileLayer(
                layer_name=layer_name,
                layer_id=layer_id, 
                layer_size=layer_size,
                layer_offset=layer_offset,
                layer_bitmap=layer_bitmap,
                layer_properties=layer_properties,
                tile_size=self.tilesize
            )

            tile_layers.append(tilelayer)

        self.layers.extend(tile_layers)
            

    def load_imagelayers(self, data:list):
        """Load a list of imagelayers in the level"""

        image_layers: list = []
        for layer in data["layers"]:
            
            # Skip non-image layers
            if layer["type"] != "imagelayer": continue


            # Get imagelayer information
            layer_id:         int = layer["id"]
            layer_name:       str = layer["name"]
            layer_image_path: str = layer["image"]
            layer_offset:     tuple = (layer["offsetx"], layer["offsety"])  if "offsetx" in layer else (0,0)
            layer_pallerax:   tuple = (layer["palleraxx"] if "palleraxx" in layer else 1, layer["palleraxy"] if "palleraxy" in layer else 1)
            layer_properties: dict  = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load ImageLayer
            imagelayer: ImageLayer = ImageLayer(
                layer_name=layer_name,
                layer_id=layer_id,
                layer_image_path=layer_image_path,
                layer_offset=layer_offset,
                layer_pallerax=layer_pallerax,
                layer_properties=layer_properties
            )

            image_layers.append(imagelayer)

        self.layers.extend(layers)


    def load_entitylayers(self, data:list):
        """Load a list of entitylayers in the level"""


        entity_layers: list = []
        for layer in data["layers"]:

            # Skip non-objectlayers & non-entitylayers
            if layer["type"]  != "objectlayer": continue
            if layer["class"] != "entity": continue


            # Get objectlayer information
            layer_id:         int  = layer["id"]
            layer_name:       str  = layer["name"]
            layer_entities:   list = layer["objects"]
            layer_properties: dict  = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load objectlayer
            entitylayer: EntityLayer = EntityLayer(
                layer_name=layer_name,
                layer_id=layer_id,
                layer_entities=layer_entities,
                layer_properties=layer_properties
            )

            entity_layer.append(entity_layer)
        
        self.layers.extend(entity_layers)


    def load_lightinglayers(self):
        """Load a list of lightinglayers in the level"""


        lighting_layers: list = []
        for layer in data["layers"]:

            # Skip non-objectlayers & non-lightinglayers
            if layer["type"]  != "objectlayer": continue
            if layer["class"] != "lighting": continue


            # Get objectlayer information
            layer_id:         int  = layer["id"]
            layer_name:       str  = layer["name"]
            layer_lights:     list = layer["objects"]
            layer_properties: dict = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load lightinglayer
            lightinglayer: LightingLayer = LightingLayer(
                
            )

            lighting_layers.append(lightinglayer)
        
        self.layers.extend(lighting_layer)



    def load_colliderlayers(self):
        pass




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
        self.layers:     list  = []             # [layer1, layer2, layer3]      

    def init_load(self):
        self.load_information(data=self.level_data)
        self.TILELAYER_load_tilesets(data=self.level_data)
        self.load_tilelayers(data=self.level_data["layers"])
        self.load_imagelayers(data=self.level_data["layers"])
        self.load_entitylayers(data=self.level_data["layers"])
        self.load_lightinglayers(data=self.level_data["layers"])
        self.load_draworder(data=self.level_data["layers"])
        self.load_graphics(data=self.level_data["layers"])
        self.ENTITYLAYER_load_canvas_id()
        self.LIGHTINGLAYER_load_canvas_id()
        self.draw_static_layers()


    # Layer specific #

    def TILELAYER_load_tilesets(self, data:dict):
        """TILELAYER pre load - get tilesets for rendering"""


        tilesets: dict = {}     # {bitmapid: (spritesheet <str> textureindex <int>)}
        for til in data["tilesets"]:

            # Get tileset information relating to level
            firstgrid: int = til["firstgid"]
            source:    str = til["source"].split("/")[-1].split(".")[0]     # eg: "..\/_sprites\/spritesheet1.tsx" to "spritesheet1"   
            
            # Get number of tiles within of spritesheet
            length: int = len(self.SPRITEMODULE.spritesheets[source])

            # Match the level bitmap tile id with a spritesheet texture index
            for textureindex,bitmapid in enumerate([e for e in range(firstgrid + length)][firstgrid::]):
                tilesets[bitmapid] = (source, textureindex)
        

        # Hand tileset information to layers
        TileLayer.tilesets = tilesets


    def ENTITYLAYER_load_canvas_id(self):
        """ENTITYLAYER pre load - get the 'centre' canvas_id for rendering"""

        for layer in self.layers:
            if layer.name == "Centre": EntityLayer.canvas_id = layer.id


    def LIGHTINGLAYER_load_canvas_id(self):
        """LIGHTINGLAYER - pre load for centre & near canvasids"""

        for layer in self.layers:
            if layer.name == "Centre": LightingLayer.centre_canvas_id = layer.id        # Centre canvaslayer
            if layer.name == "Near":   LightingLayer.near_canvas_id = layer.id          # Near   canvaslayer



    # LOADING #

    def load_information(self, data:dict):
        """Load basic level information"""

        self.name     = ""
        self.size     = (data["width"], data["height"])
        self.tilesize = (data["tilewidth"], data["tileheight"])            


    def load_tilelayers(self, data:list):
        """Load a list of tilelayers in the level"""


        tile_layers: list = []
        for layer in data:
            
            # Skip non-tilelayers
            if layer["type"] != "tilelayer": continue


            # Get tilelayer information
            layer_id:         int   = layer["id"]
            layer_name:       str   = layer["name"]
            layer_size:       tuple = (layer["width"], layer["height"])
            layer_offset:     tuple = (layer["offsetx"]*self.SPRITEMODULE.scale_factor*-1, layer["offsety"]*self.SPRITEMODULE.scale_factor*-1) if "offsetx" in layer else (0, 0)
            layer_bitmap:     list  = layer["data"]
            layer_properties: dict  = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load tilelayer
            tilelayer: TileLayer = TileLayer(
                master_level=self,
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
        for layer in data:
            
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
                master_level=self,
                layer_name=layer_name,
                layer_id=layer_id,
                layer_image_path=layer_image_path,
                layer_offset=layer_offset,
                layer_pallerax=layer_pallerax,
                layer_properties=layer_properties
            )

            image_layers.append(imagelayer)

        self.layers.extend(image_layers)


    def load_entitylayers(self, data:list):
        """Load a list of entitylayers in the level"""


        entity_layers: list = []
        for layer in data:

            # Skip non-objectlayers & non-entitylayers
            if layer["type"]  != "objectgroup": continue
            if layer["class"] != "entity": continue


            # Get objectlayer information
            layer_id:         int  = layer["id"]
            layer_name:       str  = layer["name"]
            layer_entities:   list = layer["objects"]
            layer_properties: dict  = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}


            # Load objectlayer
            entitylayer: EntityLayer = EntityLayer(
                master_level=self,
                layer_name=layer_name,
                layer_id=layer_id,
                layer_entities=layer_entities,
                layer_properties=layer_properties
            )

            entity_layers.append(entitylayer)
        
        self.layers.extend(entity_layers)


    def load_lightinglayers(self, data:list):
        """Load a list of lightinglayers in the level"""

        lighting_layers: list = []
        for layer in data:

            # Skip non-objectlayers & non-lightinglayers
            if layer["type"]  != "objectgroup": continue
            if layer["class"] != "lighting": continue


            # Get objectlayer information
            layer_id:         int  = layer["id"]
            layer_name:       str  = layer["name"]
            layer_lights:     list = layer["objects"]
            layer_properties: dict = {prop["name"]: prop["value"] for prop in layer["properties"]} if "properties" in layer else {}
            

            # Load lightinglayer
            lightinglayer: LightingLayer = LightingLayer(
                master_level=self,
                layer_name=layer_name,
                layer_id=layer_id,
                layer_lights=layer_lights,
                layer_properties=layer_properties
            )

            lighting_layers.append(lightinglayer)

        self.layers.extend(lighting_layers)


    def load_colliderlayers(self, data:list):
        pass


    def load_graphics(self, data:list):
        """Registers canvases to GRAPHICSMODULE"""

        # Register canvases
        for layer in self.layers:

            # Don't register canvas if layer is not tilelayer || imagelayer
            if Level.get_class_type(object=layer) not in ["TileLayer", "ImageLayer"]: continue

            self.GRAPHICSMODULE.register_canvas(name=layer.id, size=self.GRAPHICSMODULE.canvases["main"].size, channels=4)


    def load_draworder(self, data:list):
        """Gets the layer draw order"""
    
        # Get draw order
        draw_order: list = []
        for raw_layer in data:
            layer_name: str = raw_layer["name"]

            for i,realayer in enumerate(self.layers):
                if realayer.name == layer_name: draw_order.append(i)

        # Sort layers into draworder
        ordered_layers: list = []
        for i in draw_order:
            ordered_layers.append(self.layers[i])

        self.layers = ordered_layers


    def draw_static_layers(self):
        """Prepares static canvas resources by drawing them"""


        for layer in self.layers:
            
            # Draw TileLayers & ImageLayers
            if Level.get_class_type(object=layer) in ["TileLayer", "ImageLayer"]: 
                layer.draw(canvas=self.GRAPHICSMODULE.canvases[layer.id])


    # GAME

    def update(self):
        pass


    def draw(self):
        """Level draw() method to blit level onto GRAPHICS canvases"""

        # Blit layers onto canvases
        for layer in self.layers:

            if Level.get_class_type(layer) == "TileLayer" and layer.properties["draw_static"] == False: layer.draw(canvas=self.GRAPHICSMODULE.canvases[layer.id])                   # Non-static draw TileLayer
            if Level.get_class_type(layer) == "ImageLayer": layer.draw(canvas=self.GRAPHICSMODULE.canvases[layer.id])                                                               # draw ImageLayer
            if Level.get_class_type(layer) == "EntityLayer": layer.draw(canvas=self.GRAPHICSMODULE.canvases[EntityLayer.canvas_id])                                                             # draw EntityLayer
            if Level.get_class_type(layer) == "LightingLayer" and layer.name == "Centre lighting": layer.draw(canvas=self.GRAPHICSMODULE.canvases[LightingLayer.centre_canvas_id])  # draw centre-LightingLayer
            if Level.get_class_type(layer) == "LightingLayer" and layer.name == "Near lighting":   layer.draw(canvas=self.GRAPHICSMODULE.canvases[LightingLayer.near_canvas_id])    # draw near-LightingLayer
            if Level.get_class_type(layer) == "ShaderLayer": pass            

        
    def garbage_cleanup(self):
        pass

    
    @staticmethod
    def get_class_type(object):
        return object.__class__.__name__



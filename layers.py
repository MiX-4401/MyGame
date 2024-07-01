


class TileLayer:
    def __init__(self, layer_name:str, layer_id:int, layer_size:tuple, layer_offset:tuple, layer_bitmap:list, layer_properties:dict):
        self.name:       str   = layer_name
        self.id:         int   = layer_id,
        self.size:       tuple = layer_size
        self.offset:     tuple = layer_offset
        self.bitmap:     list  = layer_bitmap
        self.properties: dict  = layer_properties


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
    def __init__(self):
        self.lights
        self.properties


class CollisionLayer:
    def __init__(self):
        pass





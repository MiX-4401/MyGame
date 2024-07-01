


class TileLayer:
    def __init__(self, layer_id:int, layer_size:tuple, layer_offset:tuple, layer_bitmap:list, **kwargs):
        self.id:     int   = layer_id,
        self.size:   tuple = layer_size
        self.offset: tuple = layer_offset
        self.bitmap: list  = layer_bitmap


class ImageLayer:
    def __init__(self, layer_id:int, layer_image_path:str, layer_offset:tuple, layer_pallerax:tuple, **kwargs):
        self.id:          int   = layer_id
        self.image_path:  str   = layer_image_path
        self.offset:      tuple = layer_offset
        self.pallerax:    tuple = layer_pallerax


class EntityLayer:
    def __init__(self):
        self.entities
        self.canvas
        self.properties


class LightingLayer:
    def __init__(self):
        self.lights
        self.properties


class CollisionLayer:
    def __init__(self):
        pass





from json import load
from sprites  import Sprites
from graphics import Graphics
from levels   import Level


class World:
    def __init__(self, SpriteModule:Sprites, GraphicsModule:Graphics):
        
        self.SPRITEMODULE:   Sprites  = SpriteModule
        self.GRAPHICSMODULE: Graphics = GraphicsModule
        self.level_data:    dict  = {}
        self.current_level: Level = None

        self.init_load()

        self.load_level(level_name="level_1")
        self.level_start()
        
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

    def level_start(self):
        self.current_level.init_load()

    def garbage_cleanup(self):
        self.current_level.garbage_cleanup()
        




import pygame    as pg
import moderngl  as mgl
import traceback as trace
from graphics import Graphics, Texture, Canvas, Transform
from shaders  import Shaders
from sprites  import Sprites
from world    import World
from sys import exit

class Main:
    def __init__(self, screen_size:tuple, sprite_scale_factor:int, caption:str):
        self.screen_size:         tuple = screen_size
        self.caption:             str   = caption

        self.pg_clocks:    dict = {}
        self.modules:      dict = {}
    
        self.time: int = 0
        self.fps:  int = 0

        self.load_graphics()
        self.load_modules(sprite_scale_factor=sprite_scale_factor)
        
        self.modules["shaders"].create_program(title="shader", vert=self.modules["shaders"].shaders["vert"]["main"], frag=self.modules["shaders"].shaders["frag"]["shader"])
        self.modules["shaders"].create_vao(title="shader", program="shader", buffer="main", args=["2f 2f", "bPos", "bTexCoord"])

        self.run()

    def load_graphics(self):

        # Load the graphics module
        self.modules["graphics"]: Graphics = Graphics()

        # Pygame Boilerplate
        self.pg_clocks["main"]: pg.time.Clock = pg.time.Clock()
        self.modules["graphics"].pg_surfaces["main"]: pg.Surface = pg.display.set_mode(self.screen_size, pg.DOUBLEBUF | pg.OPENGL)
        pg.display.set_caption(self.caption)

        # Moderngl Boilerplate
        self.modules["graphics"].load_init()

    def load_modules(self, sprite_scale_factor:int):
        self.modules["shaders"]: Shaders = Shaders(self.modules["graphics"].ctx)                                                 # Load 'Shaders' module
        self.load_graphics_api()
        self.modules["sprites"]: Sprites = Sprites(scale_factor=sprite_scale_factor)                                                                         # Load 'Sprites' module
        self.modules["world"]:   World   = World(SpriteModule=self.modules["sprites"], GraphicsModule=self.modules["graphics"])  # Load 'World' module

    def load_graphics_api(self):
        
        # Load graphics-api resources
        self.modules["shaders"].create_program(title="display", vert=self.modules["shaders"].shaders["vert"]["display"], frag=self.modules["shaders"].shaders["frag"]["display"])
        self.modules["shaders"].create_program(title="blit",    vert=self.modules["shaders"].shaders["vert"]["blit"],    frag=self.modules["shaders"].shaders["frag"]["display"])
        self.modules["shaders"].create_program(title="flip",    vert=self.modules["shaders"].shaders["vert"]["flip"],    frag=self.modules["shaders"].shaders["frag"]["display"])
        self.modules["shaders"].create_vao(title="display", program="display", buffer="main", args=["2f 2f", "bPos", "bTexCoord"])
        self.modules["shaders"].create_vao(title="blit",    program="blit",    buffer="main", args=["2f 2f", "bPos", "bTexCoord"])
        self.modules["shaders"].create_vao(title="flip",    program="flip",    buffer="main", args=["2f 2f", "bPos", "bTexCoord"])

        # Load graphics-api
        Texture.init(ctx=self.modules["graphics"].ctx, program=self.modules["shaders"].programs["blit"], vao=self.modules["shaders"].vaos["blit"])
        Canvas.init( ctx=self.modules["graphics"].ctx, program=self.modules["shaders"].programs["blit"], vao=self.modules["shaders"].vaos["blit"])
        Transform.init(
            ctx=self.modules["graphics"].ctx, 
            programs={
                "scale": self.modules["shaders"].programs["display"],
                "flip":  self.modules["shaders"].programs["flip"]
            },
            vaos={
            "scale": self.modules["shaders"].vaos["display"],
            "flip":  self.modules["shaders"].vaos["flip"]
            }
        )

        self.modules["graphics"].canvases["main"] = Canvas.load(
            size=self.modules["graphics"].pg_surfaces["main"].get_size(),
            channels=3
        )


    def garbage_cleanup(self):
        print("============GARBAGE=============")

        for module in self.modules:
            self.modules[module].garbage_cleanup()

        self.modules["graphics"].ctx.release()

        print("Exit Complete")
 
        pg.quit()
        exit()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.garbage_cleanup()

    def update(self):
        self.fps = self.pg_clocks["main"].get_fps()
        pg.display.set_caption(f"Game | FPS: {round(self.fps)}")

        self.time += 1

    def draw(self):

        # Clear 'main' canvas
        self.modules["graphics"].canvases["main"].clear()

        # TESTING
        # self.modules["sprites"].spritesheets["spritesheet1"][3].shader(program=self.modules["shaders"].programs["shader"], vao=self.modules["shaders"].vaos["shader"], uniforms={"uTime": self.time})
        # self.modules["graphics"].canvases[2].shader(
        #     program=self.modules["shaders"].programs["shader"],
        #     vao=self.modules["shaders"].vaos["shader"],
        #     uniforms={"uTime": self.time}
        # )
        # self.modules["sprites"].spritesheets["spritesheet1"][2].shader(
        #     program=self.modules["shaders"].programs["shader"],
        #     vao=self.modules["shaders"].vaos["shader"],
        #     uniforms={"uTime": self.time}
        # )

        self.modules["world"].current_level.draw()
        self.modules["graphics"].draw()

        # Blit 'main' canvas onto screen
        self.modules["graphics"].ctx.screen.use()
        self.modules["graphics"].canvases["main"].use()
        self.modules["shaders"].vaos["main"].render(mode=mgl.TRIANGLE_STRIP)

        pg.display.flip()


    def run(self):
        while True:
            try:
                self.check_events()
                self.update()
                self.draw()
                self.pg_clocks["main"].tick(60)
            except Exception as e:
                print("===============ERROR===============")
                print(f"Error:      {e}\n")
                trace.print_exc()

                self.garbage_cleanup()



if __name__ == "__main__":
    main: Main = Main(screen_size=(1920//1.5, 1080//1.5), sprite_scale_factor=3, caption="Game")





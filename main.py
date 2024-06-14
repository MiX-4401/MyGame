import pygame   as pg
import moderngl as mgl
import traceback as trace
from sys import exit
from graphics import *
from shaders import *
from sprites import *

class Main:
    def __init__(self, screen_size:tuple, caption:str):
        self.screen_size: tuple = screen_size
        self.caption:     str   = caption

        self.pg_clocks:    dict = {}
        self.modules:      dict = {}
    
        self.time: int = 0
        self.fps:  int = 0

        self.load_graphics()
        self.load_modules()

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

    def load_modules(self):
        self.modules["shaders"]: Shaders = Shaders(self.modules["graphics"].ctx)    # Load 'Shaders' module
        self.modules["sprites"]: Sprites = Sprites()                                # Load 'Sprites' module

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

        # Reset main pg surface
        self.modules["graphics"].pg_surfaces["main"].fill(color=(0,0,0,225))

        #TEST#
        self.modules["graphics"].pg_surfaces["main"].blit(
            source=self.modules["sprites"].spritesheets["spritesheet1"][0],
            dest=(0,0)
        )

        # Write pg surface to mgl texture
        self.modules["graphics"].mgl_textures["main"].write(
            data=self.modules["graphics"].pg_surfaces["main"].get_view("1")
        )

        # Render texture to screen
        self.modules["graphics"].ctx.screen.use()
        self.modules["graphics"].mgl_textures["main"].use(location=0)
        self.modules["shaders"].programs["main"]["uTexture"] = 0
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
    main: Main = Main(screen_size=(600, 500), caption="Game")





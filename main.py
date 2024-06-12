import pygame   as pg
import moderngl as mgl
from graphics import *
from shaders import *
from sys import exit

class Main:
    def __init__(self, screen_size:tuple, caption:str):
        self.screen_size: tuple = screen_size
        self.caption:     str   = caption

        self.pg_clocks:    dict = {}
        self.modules:      dict = {}
    
        self.time: int = 0
        self.fps:  int = 0


        # Load the graphics module
        self.modules["graphics"]: Graphics = Graphics()

        # Pygame Boilerplate
        self.pg_clocks["main"]: pg.time.Clock = pg.time.Clock()
        self.modules["graphics"].pg_surfaces["main"]: pg.Surface = pg.display.set_mode(self.screen_size, pg.DOUBLEBUF | pg.OPENGL)
        pg.display.set_caption(self.caption)

        # Load additional modules
        self.modules["graphics"].create_context(title="main", auxiliary=False)
        self.modules["shaders"]: Shaders  = Shaders(self.modules["graphics"].mgl_contexts["main"])

        # Moderngl Boilerplate
        self.modules["graphics"].mgl_contexts["main"].enable(mgl.BLEND)
        self.modules["graphics"].create_texture(title="main", size=self.modules["graphics"].pg_surfaces["main"].get_size(), components=4, swizzle="BGRA", method=mgl.NEAREST)
        self.modules["graphics"].create_framebuffer(title="main", attachments=[self.modules["graphics"].mgl_textures["main"]])
        self.modules["graphics"].mgl_textures["main"].write(data=self.modules["graphics"].pg_surfaces["main"].get_view("1"))
        self.c: list = [0,0,0]
        self.run()

    def garbage_cleanup(self):
        for module in self.modules:
            self.modules[module].garbage_cleanup()

        for cont in self.modules["graphics"].mgl_contexts:
            self.modules["graphics"].mgl_contexts[cont].release()
            print("Main: releasing: {} @ {}".format(cont, self.modules["graphics"].mgl_contexts[cont]))

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

    def draw(self):
        
        self.modules["graphics"].pg_surfaces["main"].fill(color=(0,0,0))

        self.modules["graphics"].mgl_textures["main"].write(
            self.modules["graphics"].pg_surfaces["main"].get_view("1")
        )

        self.modules["graphics"].mgl_contexts["main"].screen.use()
        self.modules["graphics"].mgl_contexts["main"].screen.clear()
        self.modules["graphics"].mgl_textures["main"].use(location=0)
        self.modules["shaders"].programs["main"]["uTexture"] = 0 
        self.modules["shaders"].vaos["main"].render(mode=mgl.TRIANGLE_STRIP)

        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.pg_clocks["main"].tick(60)
            

if __name__ == "__main__":
    main: Main = Main(screen_size=(600, 500), caption="Game")





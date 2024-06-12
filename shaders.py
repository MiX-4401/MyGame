import moderngl as mgl
from numpy import array

class Shaders:
    def __init__(self, ctx:mgl.Context):
        
        self.ctx: mgl.Context = ctx

        
        self.programs:      dict = {}
        self.vaos:          dict = {}
        self.buffers:       dict = {}

        self.shaders: dict = {
            "vert": {},
            "frag": {}
        }
        
        self.load_shaders(paths=(
            r"_shaders\main.vert",
            r"_shaders\main.frag"
        ))

        self.load_base_shader()
        

    def load_shaders(self, paths:tuple):

        for path in paths:            
            
            name: str; extension: str
            name, extension = path.split("\\")[-1].split(".")
            if extension not in ["vert", "frag"]: raise BaseException("extension not compatible")

            with open(file=path, mode="r") as f:
                data = f.read()
                self.shaders[extension].update({name: data})   

    def load_base_shader(self):
        self.create_program(title="main", vert=self.shaders["vert"]["main"], frag=self.shaders["frag"]["main"])
        self.create_buffer(title="main", data=array([-1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, -1.0, 1.0, 1.0], dtype="f4"))
        self.create_vao(title="main", program="main", buffer="main", args=["2f 2f", "bPos", "bTexCoord"])

    def create_program(self, title:str, vert:str, frag:str):
        self.programs[title]: mgl.Program = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
    
    def create_vao(self, title:str, program:str, buffer:str, args:list=[]):
        self.vaos[title]: mgl.VertexArray = self.ctx.vertex_array(self.programs[program], [(self.buffers[buffer], *args)])
        
    def create_buffer(self, title:str, data:array):
        self.buffers[title]: mgl.Buffers = self.ctx.buffer(data=data)
        
    def garbage_cleanup(self):

        for buff in self.buffers:
            self.buffers[buff].release()
            print(f"Shaders: releasing: {buff} @ {self.buffers[buff]}")

        for vao in self.vaos:
            self.vaos[vao].release()
            print(f"Shaders: releasing: {vao} @ {self.vaos[vao]}")

        for prog in self.programs:
            self.programs[prog].release()
            print(f"Shaders: releasing: {prog} @ {self.programs[prog]}")
        
        


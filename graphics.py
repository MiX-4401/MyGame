import moderngl as mgl

class Graphics:
    def __init__(self):

        self.pg_surfaces:       dict = {}
        self.mgl_contexts:      dict = {}
        self.mgl_framebuffers:  dict = {}
        self.mgl_textures:      dict = {}

    def create_context(self, title:str, auxiliary:bool=False):
        if not auxiliary:
            self.mgl_contexts[title]: mgl.Context = mgl.create_context()
        else:
            self.mgl_contexts[title]: mgl.Context = mgl.create_standalone_context()

    def create_framebuffer(self, title:str, attachments:list=[], ctx:mgl.Context="main"):
        self.mgl_framebuffers[title]: mgl.Framebuffer = self.mgl_contexts[ctx].framebuffer(color_attachments=attachments)
    
    def create_texture(self, title:str, size:tuple, ctx:mgl.Context="main", components:int=4, method:str="nearest", swizzle:str="RGBA"):
        self.mgl_textures[title]: mgl.Texture = self.mgl_contexts[ctx].texture(size=size, components=components)
        
        self.mgl_textures[title].swizzle: str = swizzle
        if method == "nearest":
            self.mgl_textures[title].filter: tuple = (mgl.NEAREST, mgl.NEAREST)  
        elif method == "linear":
            self.mgl_textures[title].filter: tuple = (mgl.LINEAR, mgl.LINEAR)

    def sample_texture(self, texture:str, location:int=0):
        """
            Sets the sample location for a texture
        """

        self.mgl_textures[texture].use(location=location)
        
    def sample_framebuffer(self, framebuffer:str, attachment:int=0, location:int=0):
        """
            Sets the sample location for a framebuffer
        """

        self.framebuffers[framebuffer].color_attachments[attachment].use(location=location)

    def render_direct(self, program:mgl.Program, vao:mgl.VertexArray, framebuffer:mgl.Framebuffer, **uniforms):
        """
            Renders the shader directly to the framebuffer
        """

        # Ready framebuffer
        framebuffer.use()
        # self.framebuffers[framebuffer].clear()

        # Set uniforms
        for uni in uniforms:
            program[uni] = uniforms[uni]
        
        # Render
        vao.render(mgl.TRIANGLE_STRIP)

        return framebuffer

    def garbage_cleanup(self):

        for text in self.mgl_textures:
            self.mgl_textures[text].release()
            print(f"Graphics: releasing: {text} @ {self.mgl_textures[text]}")

        for frame in self.mgl_framebuffers:
            self.mgl_framebuffers[frame].release()
            print(f"Graphics: releasing: {frame} @ {self.mgl_framebuffers[frame]}")



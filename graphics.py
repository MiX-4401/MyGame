import moderngl as mgl

class Graphics:
    def __init__(self):

        self.pg_surfaces:       dict = {}
        self.mgl_framebuffers:  dict = {}
        self.mgl_textures:      dict = {}

    def load_init(self):

        # Create moderngl context
        self.ctx: mgl.Context = mgl.create_context()
        
        # Enable moderngl context settings
        self.ctx.enable(mgl.BLEND)

        # Create main 'mgl texture' from the main 'pg surface'
        self.create_texture(
            title="main", 
            size=self.pg_surfaces["main"].get_size(), 
            components=4, 
            swizzle="BGRA", 
            method=(mgl.NEAREST, mgl.NEAREST)
        )

        # Write the main 'pg surface' onto the 'mgl texture'
        self.mgl_textures["main"].write(
            data=self.pg_surfaces["main"].get_view("1")
        )

        # Bind the main 'mgl texture' to the 'main framebuffer'
        self.create_framebuffer(
            title="main", 
            attachments=[self.mgl_textures["main"]]
        )
    
    def create_framebuffer(self, title:str, attachments:list=[]):
        self.mgl_framebuffers[title]: mgl.Framebuffer = self.ctx.framebuffer(color_attachments=attachments)
    
    def create_texture(self, title:str, size:tuple, components:int=4, method:str="nearest", swizzle:str="RGBA"):
        self.mgl_textures[title]: mgl.Texture = self.ctx.texture(size=size, components=components)
        
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



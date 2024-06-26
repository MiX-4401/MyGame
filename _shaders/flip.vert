# version 460 core

uniform bool xFlip;
uniform bool yFlip;

in vec2 bPos;
in vec2 bTexCoord;
out vec2 uvs;

void main () {
    uvs = bTexCoord;

    if (xFlip == true) {
        uvs.x = 1 - uvs.x;
    };
    if (yFlip == true) {
        uvs.y = 1- uvs.y;
    };
    

    gl_Position = vec4(bPos, 0.0, 1.0);
}
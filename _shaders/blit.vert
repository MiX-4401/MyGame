# version 460 core

uniform vec2 pos;
uniform vec2 sourceSize;
uniform vec2 textureSize;

in vec2 bPos;
in vec2 bTexCoord;
out vec2 uvs;

void main () {
    uvs = bTexCoord;
    
    vec2 clipPosition = pos;
    clipPosition.x    = (2.0 * pos.x/textureSize.x) - 1;
    clipPosition.y    = 1.0 - (2.0 * pos.y / textureSize.y);
    
    vec2 scaledPos = bPos * sourceSize / textureSize;
    
    gl_Position = vec4(scaledPos + clipPosition, 0.0, 1.0);
}
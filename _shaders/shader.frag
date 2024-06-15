# version 460 core

uniform sampler2D myTexture;
uniform int uTime;

in vec2 uvs;
out vec4 fColour;

void main(){
    vec4 colour = texture(myTexture, uvs).rgba;
    fColour = vec4(1.0, uvs.x * sin(uTime * 0.01), uvs.y, 1.0);
}
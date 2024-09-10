// -*- compile-command: "x86_64-w64-mingw32-g++ -o main main.cpp -static -L lib/ -lraylib -lopengl32 -lgdi32 -lwinmm" -*-
#include <stdio.h>
#include "lib/raylib-cpp.hpp"
namespace R = raylib;

#define WIDTH 1920
#define HEIGHT 1080

#define K 0.001

int main() {
    SetTargetFPS(60);
    InitWindow(WIDTH, HEIGHT, "Raylib basic window");
    ToggleFullscreen();

    R::Vector2 position(WIDTH/2, HEIGHT/2);
    R::Vector2 velocity(0,0);

    R::Vector2 nodes[] = {
        R::Vector2(WIDTH/2, HEIGHT/4),
        R::Vector2(WIDTH/4, HEIGHT * 3 / 4),
        R::Vector2(WIDTH * 3 / 4, HEIGHT * 3 / 4),
    };
    
    
    while (!WindowShouldClose()) {

        if (IsKeyPressed(KEY_Q)) {
            nodes[1] = GetMousePosition();
        }
        if (IsKeyPressed(KEY_W)) {
            nodes[0] = GetMousePosition();
        }
        if (IsKeyPressed(KEY_E)) {
            nodes[2] = GetMousePosition();
        }
        
        velocity += (nodes[0] - position) * K;
        velocity += (nodes[1] - position) * K;
        velocity += (nodes[2] - position) * K;
        position += velocity;

        velocity *= 0.99;
        
        BeginDrawing();
        	ClearBackground(RAYWHITE);

            position.DrawCircle(30, RED);
            
            for (auto node: nodes) {
                node.DrawCircle(10, BLUE);
            }


            
        EndDrawing();    
    }

    CloseWindow();
    
    return 0;
}

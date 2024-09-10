// -*- compile-command: "x86_64-w64-mingw32-gcc -o main2 main2.c -L lib/ -lraylib -lopengl32 -lgdi32 -lwinmm" -*-
#include <stdio.h>
#include "lib/raylib.h"
#include "lib/raymath.h"
#include "lib/rlgl.h"

#define WIDTH 1920
#define HEIGHT 1080

typedef struct Body {
    Vector2 position;
    Vector2 velocity;
    Color color;
    float radius;
    float mass;
} Body;

Body createBody(Vector2 pos, Vector2 vel, Color color) {
    return (Body){pos, vel, color, 40.0, 1.0};
}

#define G (0.001)

int main() {
    SetTargetFPS(60);
    InitWindow(WIDTH, HEIGHT, "Gravity");
    ToggleFullscreen();

    
    //Vector2 CENTER = (Vector2){(float)(WIDTH/2), (float)(HEIGHT/2)};
    Vector2 CENTER = (Vector2){(float)(WIDTH/2), (float)(HEIGHT/2)};
    Vector2 initial_velocity = (Vector2){4.0824829, 0.0};
    Vector2 offset = (Vector2){0.0, 300.0};
    Body body = createBody(Vector2Add(CENTER, offset), initial_velocity, RED);
    
    RenderTexture2D target = LoadRenderTexture(WIDTH, HEIGHT);
    
    while (!WindowShouldClose()) {
        
        CENTER = GetMousePosition();
        Vector2 direction = Vector2Normalize(Vector2Subtract(CENTER, body.position));
        float dist = Vector2Length(Vector2Subtract(CENTER, body.position));
        float acceleration = (G) * (dist);
        Vector2 acceleration_vector = Vector2Scale(direction, acceleration);


        body.velocity = Vector2Add(body.velocity, acceleration_vector);
            
        body.position = Vector2Add(body.position, body.velocity);


        BeginTextureMode(target);
        	DrawCircleV(body.position, 5.0, (Color){body.color.r/2, body.color.g/2, body.color.b/2, 255});
        EndTextureMode();
        
        BeginDrawing();
        ClearBackground(BLACK);
        	DrawTexturePro(target.texture, (Rectangle){0, 0, (float)target.texture.width, -(float)target.texture.height},
                           (Rectangle){0, 0, (float)target.texture.width, (float)target.texture.height}, Vector2Zero(), 0.0, WHITE);

            //Vector2 center_of_mass = Vector2Scale((Vector2Add(Bodies[0].position, Vector2Add(Bodies[1].position, Bodies[2].position))), (1.0/3.0));
            //DrawCircleV(center_of_mass, 10.0, WHITE);
            
                            
                //DrawCircleV(body.position, 5.0, (Color){body.color.r, body.color.g, body.color.b, 128});
                //DrawTextureEx(target.texture, Vector2Zero(), 0.0, 1.0, WHITE);
                
            DrawCircleV(CENTER, 5, WHITE);
            DrawCircleV(body.position, body.radius, body.color);
                //DrawPixelV(body.position, body.color);
            
        EndDrawing();    
    }

    CloseWindow();
    
    return 0;
}

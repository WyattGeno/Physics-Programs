// -*- compile-command: "x86_64-w64-mingw32-gcc -o main main.c -L lib/ -lraylib -lopengl32 -lgdi32 -lwinmm" -*-
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

Body Bodies[3];

#define G (5000.0)

int main() {
    SetTargetFPS(60);
    InitWindow(WIDTH, HEIGHT, "Raylib basic window");
    ToggleFullscreen();

    
        Vector2 center = (Vector2){(float)(WIDTH/2), (float)(HEIGHT/2)};
        Vector2 offset = (Vector2){0.0, 300.0};
        Vector2 initial_velocity = (Vector2){3.10201619701, 0.0};
        //Bodies[0] = createBody((Vector2){200.0, 200.0}, (Vector2){1.0, 0.0}, RED);
        //Bodies[1] = createBody((Vector2){100.0, 900.0}, Vector2Zero(), BLUE);
        //Bodies[2] = createBody((Vector2){1000.0, 900.0}, (Vector2){-1.0, 0.0}, GREEN);
        Bodies[0] = createBody(Vector2Add(center, Vector2Rotate(offset, 0.0)), Vector2Rotate(initial_velocity, 0.0), RED);
        Bodies[1] = createBody(Vector2Add(center, Vector2Rotate(offset, 120.0/180.0*PI)), Vector2Rotate(initial_velocity, 120.0/180.0*PI), BLUE);
        //Bodies[1].position = Vector2Add(Bodies[1].position, (Vector2){0.0, 0.0});
        Bodies[2] = createBody(Vector2Add(center, Vector2Rotate(offset, 240.0/180.0*PI)), Vector2Rotate(initial_velocity, 240.0/180.0*PI), GREEN);
    
    
    RenderTexture2D target = LoadRenderTexture(WIDTH, HEIGHT);
    
    while (!WindowShouldClose()) {
        //for (int ii = 0; ii < 10; ii++)
        {
        for (int i = 0; i < 3; i++) {
            Body body = Bodies[i];
            Vector2 acceleration_vector = Vector2Zero();
            for (int j = 0; j < 3; j++) {
                if (i != j) {
                    Body other_body = Bodies[j];

                    Vector2 direction = Vector2Normalize(Vector2Subtract(other_body.position, body.position));
                    float dist = Vector2Length(Vector2Subtract(other_body.position, body.position));
                    float acceleration = (G * other_body.mass) / (dist * dist);
                    Vector2 new_acceleration_vector = Vector2Scale(direction, acceleration);

                    acceleration_vector = Vector2Add(acceleration_vector, new_acceleration_vector);
                }
            }
            Bodies[i].velocity = Vector2Add(Bodies[i].velocity, acceleration_vector);
        }

        for (int i = 0; i < 3; i++) {
            Bodies[i].position = Vector2Add(Bodies[i].position, Bodies[i].velocity);
        }
        }
        BeginTextureMode(target);
        	for (int i = 0; i < 3; i++) {
                Body body = Bodies[i];
                DrawCircleV(body.position, 5.0, (Color){body.color.r/2, body.color.g/2, body.color.b/2, 255});
            }
        EndTextureMode();
        
        BeginDrawing();
        ClearBackground(BLACK);
        	DrawTexturePro(target.texture, (Rectangle){0, 0, (float)target.texture.width, -(float)target.texture.height},
                           (Rectangle){0, 0, (float)target.texture.width, (float)target.texture.height}, Vector2Zero(), 0.0, WHITE);

            Vector2 center_of_mass = Vector2Scale((Vector2Add(Bodies[0].position, Vector2Add(Bodies[1].position, Bodies[2].position))), (1.0/3.0));
            DrawCircleV(center_of_mass, 10.0, WHITE);
            
            for (int i = 0; i < 3; i++) {
                Body body = Bodies[i];
                
                //DrawCircleV(body.position, 5.0, (Color){body.color.r, body.color.g, body.color.b, 128});
                //DrawTextureEx(target.texture, Vector2Zero(), 0.0, 1.0, WHITE);
                
                
                DrawCircleV(body.position, body.radius, body.color);
                //DrawPixelV(body.position, body.color);
            }
        EndDrawing();    
    }

    CloseWindow();
    
    return 0;
}

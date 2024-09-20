import pygame
import random

Vector2 = pygame.math.Vector2
Color = pygame.Color
Rect = pygame.Rect

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font("fonts/Cascadia_Mono_NF_Bold.ttf", 18)

g = 9.81 # m/s^2
Water_Density = 1000 # kg/m^3

# density = 0.5 g/c^3
# density 500 kg/m^3
cube_mass = 1500 # Kg
cube_side_length = 1 # m
cube_position = Vector2(200, 10) # cm
cube_velocity = 0 # m

water_level = 250

spring_position = 150 # cm
spring_k = 12000 # N/m

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    Net_Force = 0

    Volume_Displaced = min(max((cube_position.y + 100) - 250, 0), 100) / 100 
    Buoyant_Force = Water_Density * Volume_Displaced * g
    Net_Force -= Buoyant_Force
    
    Gravitational_Force = cube_mass * g
    Net_Force += Gravitational_Force

    Spring_Force = -spring_k * ((cube_position.y - spring_position)/100)
    Net_Force += Spring_Force
    
    Acceleration = Net_Force / cube_mass
    cube_velocity += Acceleration /60
    cube_velocity *= 0.99
    cube_position.y += (cube_velocity * 100) /60
    
    pygame.draw.rect(screen, "blue", Rect(0, 250, 500, 250))
    pygame.draw.circle(screen, "black", (250, spring_position), 10)
    pygame.draw.line(screen, "black", (250, spring_position), (250, cube_position.y), 2)
    pygame.draw.rect(screen, "red", Rect(cube_position.x, cube_position.y, 100, 100))

    
    screen.blit(font.render("Position: " + str((cube_position.y) / 100), 1, "black"), (10, 20))
    screen.blit(font.render("Velocity: " + str(cube_velocity), 1, "black"), (10, 40))
    screen.blit(font.render("Acceleration: " + str(Acceleration), 1, "black"), (10, 60))
    screen.blit(font.render("Volume Displaced: " + str(Volume_Displaced), 1, "black"), (10, 80))
    screen.blit(font.render("Spring Force: " + str(Spring_Force), 1, "black"), (10, 100))


    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

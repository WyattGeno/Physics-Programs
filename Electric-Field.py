import pygame
import random, math

Vector2 = pygame.math.Vector2
Color = pygame.Color
Rect = pygame.Rect

pygame.init()
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

font = pygame.font.Font("fonts/Cascadia_Mono_NF_Bold.ttf", 18)


class Particle:
    def __init__(self, c, p):
        self.charge = c
        self.position = p
        
Particles = []
Particles.append(Particle(1, Vector2(250, 250)))
Particles.append(Particle(-1, Vector2(750, 250)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]: Particles[0].position = Vector2(pygame.mouse.get_pos())
    if keys[pygame.K_2]: Particles[1].position = Vector2(pygame.mouse.get_pos())

    screen.fill("white")

    for particle in Particles:
        if particle.charge > 0:
            color = "red"
        elif particle.charge < 0:
            color = "blue"
        else:
            color = "black"
        pygame.draw.circle(screen, color, particle.position, 20)
    
    for particle in Particles:
        for i in range(12):
            angle = i/12 * math.pi * 2
            point = Vector2(math.cos(angle), math.sin(angle)) * 10 + particle.position

            for _ in range(5000):
                #if (point - electron_position).magnitude() < 10: break

                total_force = Vector2(0, 0)
                
                for particle2 in Particles:
                    total_force += -particle.charge * particle2.charge * (particle2.position - point).normalize() / (particle2.position - point).magnitude_squared()

                if total_force.length() == 0: break                
                pygame.draw.line(screen, "black", point, point + total_force.normalize() * 1)
                
                point = point + total_force.normalize() * 0.1

    """
    mouse_pos = pygame.mouse.get_pos()
    v_mouse_pos = Vector2(mouse_pos[0], mouse_pos[1])
    voltage = 0
    for particle in Particles:
        voltage += 1/((v_mouse_pos - particle.position).length())

    screen.blit(font.render(str(voltage), 1, "black"), (10, 10))
    """
    pygame.display.flip()

    clock.tick(60)

pygame.quit()


# TODO
# - New input for controlling particles
# - Equipotentials

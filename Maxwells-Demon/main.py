# File 1: main.py
import math
import random
from sys import exit

import pygame

Vector2 = pygame.math.Vector2

from Particle_class import Particle

WIDTH = 900
HEIGHT = 450

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN_BOUNDS = pygame.Rect(0, 0, WIDTH, HEIGHT)
pygame.display.set_caption("Maxwell's Demon")

FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18)
titleFont = pygame.font.SysFont("Arial", 50)

Particles = []
for _ in range(10):
  p = Vector2(min(max(random.random() * WIDTH, 20), WIDTH - 20),
              min(max(random.random() * HEIGHT, 20), HEIGHT - 20))
  v = Vector2(5, 0).rotate(random.random() * 360)
  r = 20
  Particles.append(Particle(p, v, r, SCREEN_BOUNDS))

time_frozen = False
barrier_activated = False

avg_momentum = 0
t = 0

intro = 0
while intro < 2:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      intro += 1

  screen.fill(pygame.Color(10, 10, 10))

  if intro == 0:
    screen.blit(titleFont.render("Maxwell's ", 1, "red"), (230, 150))
    screen.blit(titleFont.render("Demon", 1, "blue"), (260 + 230, 150))
    screen.blit(font.render("Press space to start", 1, "white"), (360, 300))
  else:
    screen.blit(
        font.render(
            "This game is a simulation of the Maxwell's Demon thought experiment.",
            1, "orange"), (40, 20))
    screen.blit(
        font.render(
            "There are two chambers of gas (represented by particles) which can be",
            1, "orange"), (40, 40))
    screen.blit(
        font.render(
            "seperated by a toggleable barrier. By opening and closing this barrier,",
            1, "orange"), (40, 60))
    screen.blit(
        font.render(
            "you can choose which particles pass between the chambers. Your goal is",
            1, "orange"), (40, 80))
    screen.blit(
        font.render(
            "to move slower particles to one chamber and hotter particles to the other,",
            1, "orange"), (40, 100))
    screen.blit(
        font.render(
            "thereby violating the second law of thermodynamics. You can also",
            1, "orange"), (40, 120))
    screen.blit(
        font.render("freeze time for convenience. Good Luck!", 1, "orange"),
        (40, 140))

  pygame.display.flip()
  clock.tick(FPS)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      time_frozen = not time_frozen

    if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
      barrier_activated = not barrier_activated

  for particle in Particles:
    particle.frame_reset(barrier_activated)

  if not time_frozen:
    for particle in Particles:
      particle.update(Particles, barrier_activated)

  screen.fill(pygame.Color(10, 10, 10))

  if barrier_activated:
    pygame.draw.line(screen, "white", (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 10)

  for particle in Particles:
    vel = particle.vel.magnitude() * 2
    color = pygame.Color(max(min(255, int(vel * 20)), 0), 0,
                         max(min(255, int(255 - vel * 20)), 0))
    pygame.draw.circle(screen, color, particle.pos, particle.rad)

    if time_frozen:
      for particle in Particles:
        pygame.draw.line(
            screen, "white", particle.pos,
            particle.pos + particle.vel.normalize() * particle.rad * 1.5)

  total_energy = 0
  energy_left = 0
  energy_right = 0
  left_particles = 0
  right_particles = 0

  for particle in Particles:
    total_energy += particle.vel.magnitude_squared() * 0.5
    if particle.pos.x < SCREEN_BOUNDS.centerx:
      left_particles += 1
      energy_left += particle.vel.magnitude_squared() * 0.5
    else:
      right_particles += 1
      energy_right += particle.vel.magnitude_squared() * 0.5

  screen.blit(font.render("Goal: Have less than 1.0 unit", 1, "orange"),
              (0, 0))
  screen.blit(font.render("of temperature on one side", 1, "orange"), (0, 20))

  screen.blit(font.render("Freeze/Unfreeze time - Space key", 1, "orange"),
              (WIDTH - 310, 0))
  screen.blit(font.render("Toggle Barrier - B key", 1, "orange"),
              (WIDTH - 310, 20))

  if (0 not in [total_energy, energy_left, left_particles]):
    energy_left = round(energy_left * 100 / total_energy, 1)
    screen.blit(
        font.render(
            "Left Temperature: " + str(round(energy_left / left_particles, 2)),
            1, "orange"), (0, HEIGHT - 25))

  if (0 not in [total_energy, energy_right, right_particles]):
    energy_right = round(energy_right * 100 / total_energy, 1)
    screen.blit(
        font.render(
            "Right Temperature: " +
            str(round(energy_right / right_particles, 2)), 1, "orange"),
        (WIDTH / 2 + 10, HEIGHT - 25))

  t += 1
  pygame.display.flip()
  clock.tick(FPS)

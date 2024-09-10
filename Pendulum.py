import pygame
from sys import exit
import math, random

PI = math.pi

WIDTH = 900
HEIGHT = 500

Vector2 = pygame.math.Vector2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pendulum")
FPS = 60
clock = pygame.time.Clock()

pivot_position = Vector2(WIDTH / 2, HEIGHT / 4)

L = 200
theta = PI / 4
v = 0
g = -1000

dt = 1 / FPS

last_vector_positions = [Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)]
last_positions = [0.0, 0.0, 0.0]
positions_list = []
velocities_list = []
accelerations_list = []

t = 0

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  screen.fill("white")

  # Calculate new acceleration, velocity, and position
  a = g / L * math.sin(theta)
  pixel_acceleration = g * math.sin(theta)

  v += a * dt
  v *= 1

  theta += v * dt

  # Constain theta from -PI to PI
  if theta > PI:
    theta -= 2 * PI
  elif theta < -PI:
    theta += 2 * PI

  ## Display pendulum
  # Position of bob relative to pivot
  pendulum_rel_pos = L * Vector2(math.sin(theta), math.cos(theta))
  # Draw arm
  pygame.draw.line(screen, "black", pivot_position,
                   pivot_position + pendulum_rel_pos)
  # Draw pivot
  pygame.draw.circle(screen, "black", pivot_position, 3)
  # Draw bob
  bob_position = pivot_position + pendulum_rel_pos
  pygame.draw.circle(screen, "black", bob_position, 15)

  # Calculate the vector acceleration
  
  last_positions.pop(0)
  last_positions.append(theta * L)
  last_vector_positions.pop(0)
  last_vector_positions.append(bob_position)
  last_v = (last_vector_positions[2] - last_vector_positions[1]) / dt
  last_v2 = (last_vector_positions[1] - last_vector_positions[0]) / dt
  calculated_vector_acceleration = (last_v - last_v2) / dt

  '''
  # Update lists
  positions_list.append(theta)
  velocities_list.append(v)
  accelerations_list.append(calculated_vector_acceleration.magnitude())
  '''

  # Calculate other force/acceleration vectors
  gravity_vector = Vector2(0, -g)
  perpendicular_vector = calculated_vector_acceleration - gravity_vector

  # Draw Force diagram and velocity vectors
  pygame.draw.line(screen, "orange", bob_position,
                   bob_position + calculated_vector_acceleration / 15, 5)
  pygame.draw.line(screen, "red", bob_position,
                   bob_position + gravity_vector / 15, 5)
  pygame.draw.line(screen, "red", bob_position,
                   bob_position + perpendicular_vector / 15, 5)
  pygame.draw.line(screen, "blue", bob_position, bob_position + last_v / 15, 5)
  '''
  # Draw graphs for position, velocity, and acceleration
  while len(positions_list) > WIDTH:
    positions_list.pop(0)
  for i in range(len(positions_list) - 1):
    pygame.draw.line(screen, "green",
                     Vector2(i, positions_list[i] * 50 + HEIGHT / 2),
                     Vector2(i + 1, positions_list[i + 1] * 50 + HEIGHT / 2),
                     2)
  while len(velocities_list) > WIDTH:
    velocities_list.pop(0)
  for i in range(len(velocities_list) - 1):
    pygame.draw.line(screen, "blue",
                     Vector2(i, velocities_list[i] * 50 + HEIGHT / 2),
                     Vector2(i + 1, velocities_list[i + 1] * 50 + HEIGHT / 2),
                     2)
  while len(accelerations_list) > WIDTH:
    accelerations_list.pop(0)
  for i in range(len(accelerations_list) - 1):
    pygame.draw.line(
        screen, "orange", Vector2(i, HEIGHT / 2 - accelerations_list[i] / 10),
        Vector2(i + 1, HEIGHT / 2 - accelerations_list[i + 1] / 10), 2)
  # print(calculated_vector_acceleration.magnitude())
  # print(len(accelerations_list))
  '''
  pygame.display.flip()
  #t += 1
  clock.tick(FPS)

# TO DO:
# - Measure the relationship between some variables and the tension of the arm
# ex. current velocity of bob and current tension

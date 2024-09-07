# file 2: Particle_class.py
import math
import random
from sys import exit

import pygame

Vector2 = pygame.math.Vector2


def find_collision_positions(a0: Vector2, b0: Vector2, af: Vector2,
                             bf: Vector2, ra: float, rb: float):
  A = (af.x - a0.x - bf.x + b0.x)**2 + (af.y - a0.y - bf.y + b0.y)**2
  B = (2 * (a0.x - b0.x) * (af.x - a0.x - bf.x + b0.x) + 2 * (a0.y - b0.y) *
       (af.y - a0.y - bf.y + b0.y))
  C = (a0.x - b0.x)**2 + (a0.y - b0.y)**2 - (ra + rb)**2

  DISC = B**2 - 4 * A * C
  if DISC <= 0:
    # print("No collision (no solution)")
    return None

  t1 = (-1 * B + math.sqrt(DISC)) / (2 * A)
  t2 = (-1 * B - math.sqrt(DISC)) / (2 * A)

  if t2 < t1:
    temp = t2
    t2 = t1
    t1 = temp

  # print("t1:", t1)
  # print("t2:", t2)

  if t1 < 0:
    # print("No collision in time interval (t1 < 0)")
    return None

  if t1 > 1:
    # print("No collision in time interval (t1 > 1)")
    return None

  # print("return value:", t1)
  return t1


def calculate_new_velocities(particle, other_particle):

  vel1 = particle.vel
  vel2 = other_particle.vel
  pos1 = particle.pos
  pos2 = other_particle.pos
  mass1 = 1
  mass2 = 1

  return calculate_velocity(vel1, vel2, pos1, pos2, mass1,
                            mass2), calculate_velocity(vel2, vel1, pos2, pos1,
                                                       mass2, mass1)


def calculate_velocity(v1, v2, p1, p2, m1, m2):
  return v1 - (2 * m2 / (m1 + m2)) * (v1 - v2).dot(p1 - p2) / (
      p1 - p2).magnitude()**2 * (p1 - p2)


class Particle:

  def __init__(self, pos, vel, rad, BOUNDS):
    self.pos = pos
    self.vel = vel
    self.rad = rad
    self.moved_this_frame = False
    self.BOUNDS = BOUNDS
    self.side = ""

  def update(self, particle_list, barrier_activated):
    self.motion()
    self.collision(particle_list, barrier_activated)
    self.moved_this_frame = True

  def frame_reset(self, barrier_activated):
    self.moved_this_frame = False

    particle_rect = self.get_rect()
    if barrier_activated and (self.side == ""):
      if particle_rect.centerx < self.BOUNDS.centerx:
        self.side = "left"
      else:
        self.side = "right"
    elif (not barrier_activated) and not (self.side == ""):
      self.side = ""

  def motion(self):
    self.pos = self.pos + self.vel

  def collision(self, particle_list, barrier_activated):
    if self.check_boundary(): self.boundary_collision()
    self.particle_collision(particle_list)
    if barrier_activated: self.barrier_collision()

  def get_rect(self):
    top_left = self.pos - Vector2(self.rad, self.rad)
    return pygame.Rect(top_left.x, top_left.y, 2 * self.rad, 2 * self.rad)

  def check_boundary(self):
    particle_rect = self.get_rect()
    return not self.BOUNDS.contains(particle_rect)

  def boundary_collision(self):
    particle_rect = self.get_rect()

    if particle_rect.top < self.BOUNDS.top and self.vel.y < 0:
      self.pos.y = -self.pos.y + 2 * self.rad
      self.vel.y = -self.vel.y
    elif particle_rect.bottom > self.BOUNDS.bottom and self.vel.y > 0:
      self.pos.y = 2 * self.BOUNDS.bottom - (self.pos.y + self.rad) - self.rad
      self.vel.y = -self.vel.y
    if particle_rect.left < self.BOUNDS.left and self.vel.x < 0:
      self.pos.x = -particle_rect.left + self.rad
      self.vel.x = -self.vel.x
    elif particle_rect.right > self.BOUNDS.right and self.vel.x > 0:
      self.pos.x = 2 * self.BOUNDS.right - particle_rect.right - self.rad
      self.vel.x = -self.vel.x

  def particle_collision(self, particle_list):
    for i in range(len(particle_list)):
      other_particle = particle_list[i]
      if other_particle is self:
        continue

      # print("  Other Particle:", i)

      if other_particle.moved_this_frame:
        bf = other_particle.pos
        b0 = other_particle.pos - other_particle.vel
      else:
        bf = other_particle.pos + other_particle.vel
        b0 = other_particle.pos

      a0 = self.pos - self.vel
      af = self.pos

      ra = self.rad
      rb = other_particle.rad

      t = find_collision_positions(a0, b0, af, bf, ra, rb)
      # print("    t value:", t)
      if t is None:
        continue

      self.pos = a0 + t * (af - a0)
      other_particle.pos = b0 + t * (bf - b0)

      self.vel, other_particle.vel = calculate_new_velocities(
          self, other_particle)

  def barrier_collision(self):
    particle_rect = self.get_rect()
    if (self.side == "left") and (particle_rect.right
                                  > self.BOUNDS.centerx) and (self.vel.x > 0):
      self.pos.x = 2 * self.BOUNDS.centerx - particle_rect.right - self.rad
      self.vel.x = -self.vel.x
    elif (self.side == "right") and (particle_rect.left
                                     < self.BOUNDS.centerx) and (self.vel.x
                                                                 < 0):
      self.pos.x = 2 * self.BOUNDS.centerx - particle_rect.left + self.rad
      self.vel.x = -self.vel.x

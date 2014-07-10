from ndemo import *
from sims import *
import numpy as np
import random

class VBoidCage(VWorld, BoidCage):
    pass

w = VBoidCage(wh=(500, 500), size=(2550, 2550, 2550))
for _ in range(10):
    pos = (random.random()*255, random.random()*255, random.random()*255)
    vel = (random.random(), random.random(), random.random())
    w.insert(Boid(pos=pos, vel=vel))

while 1:
    w.draw()
    w.world_step(1)
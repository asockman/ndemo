from ndemo import *
from sims import *
import pygame, sys

class VNewtCage(VWorld, NewtCage):
    pass
class PygameNewtCage(PygameWorld, NewtCage):
    pass

d = PygameNewtCage((500, 500),(255, 255, 255), fill=(50,50,50))
b = VNewtCage((500, 500),(255, 255, 255))
b.screen.center = (255/2, 255/2, 255/2)
b.argfuncs['color'] = lambda o: (o.pos[2]/255,0,1-o.pos[2]/255)
b.argfuncs['radius'] = lambda o: 5
d.argfuncs['color'] = lambda o: (o.pos[2],0,255-o.pos[2])
d.argfuncs['pos'] = lambda o: np.array((o.pos[0]*2,500-o.pos[1]*2), dtype='int')
p = Newt((255/2, 255/2, 255/2), mass=1500)
d.attractors.add(p)
b.attractors.add(p)
d.insert(p)
b.insert(p)

for po in range(3):
    for ve1 in range(3):
        for ve2 in range(2):
            pot = [200, 200, 200]
            pot[po] = 70
            vet = [0, 0, 0]
            vet[ve1] = -1
            if not ve2: ve2 -= 1
            vet[(ve1+ve2)%3] = -2
            o = Newt(pot, vet, mass=1)
            d.insert(o)
            b.insert(o)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    d.draw()
    b.draw()
    for _ in range(100):
        d.world_step(0.001)

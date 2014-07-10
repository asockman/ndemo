from ndemo import *
from sims import *
import pygame, sys

class VNewtCage(VWorld, NewtCage):
    pass
class PygameNewtCage(PygameWorld, NewtCage):
    pass

d = PygameNewtCage(fill=(50,50,50))
b = VNewtCage()

b.argfuncs['color'] = lambda o: (o.pos[2]/255,0,1-o.pos[2]/255)
b.argfuncs['radius'] = lambda o: 5
d.argfuncs['color'] = lambda o: (o.pos[2],0,255-o.pos[2])
d.argfuncs['pos'] = lambda o: np.array((o.pos[0]*2,500-o.pos[1]*2), dtype='int')
p = Newt((255/2, 255/2, 255/2), mass=1000)
x = Newt((200, 200, 70), (-2, 0, 0), mass=1)
y = Newt((200, 70, 200), (0, 0, -2), mass=1)
z = Newt((70, 200, 200), (0, -2, 0), mass=1)
d.attractors.add(p)
b.attractors.add(p)
d.insert(p, x, y, z)
b.insert(p, x, y, z)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    d.draw()
    b.draw()

    for _ in range(100):
        b.world_step(0.001)

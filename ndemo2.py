from ndemo import *
import pygame
class VNewtCage(VWorld, NewtCage):
    pass
d = PygameNewtCage((500, 500),(255, 255, 255, 255), fill=(50,50,50))
b = VNewtCage((500, 500), (255, 255, 255, 255))

b.argfuncs['radius'] = lambda o: 5
d.argfuncs['pos'] = lambda o: np.array((o.pos[0]*2,500-o.pos[1]*2), dtype='int')
p = Newt((255/2, 255/2, 255/2, 255/2), mass=1000)
x = Newt((130, 200, 70, 200), (-2, 0, 0, -1), mass=1)
y = Newt((200, 70, 200, 130), (0, 0, -1, -2), mass=1)
z = Newt((70, 200, 130, 200), (0, -1, -2, 0), mass=1)
a = Newt((200, 130, 200, 70), (-1, -2, 0, 0), mass=1)
d.attractors.add(p)
b.attractors.add(p)
d.insert(p, x, y, z, a)
b.insert(p, x, y, z, a)
d.argfuncs['color'] = lambda o: (0,255-np.sqrt(np.sum((o.pos - p.pos)**2)),0)
b.argfuncs['color'] = lambda o: (0,255-np.sqrt(np.sum((o.pos - p.pos)**2)),0)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    d.draw()
    b.draw()
    for _ in range(100):
        d.world_step(0.001)

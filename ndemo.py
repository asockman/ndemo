"""
a toolkit for programming in the nth-Dimension


"""
# agrippa kellum : sep 2013

__all__ = ['World', 'PygameWorld', 'VWorld']

import numpy as np

class World(object):
    ''' An nth-dimensional prism in which objects may be handled

    Input:
        size - an array-like of dimensions
            (examples:)
                (200, 400) : a 2d rectangle
                (100, 100, 100) : a 3d cube
                (50, 50, 50, 50) : a 4d hypercube
    '''
    #im renouncing positional arguments. viva la keyvolution.
    def __init__(self, size=(255, 255, 255)):
        self.size = np.array(size)
        self.d = len(size)
        self.objects = set() #consider sets

    def world_step(self, dt):
        ''' applies one step of iteration to the world for time step dt '''
        for object in self.objects:
            object.step(dt)

    def insert(self, *objs):
        ''' inserts an object into the world
        may just be useless
        '''
        for object in objs:
            if object.d == self.d:
                self.objects.add(object)
                object.world = self
            else:
                raise ValueError("object exists in different dimension from world")
                # considering removing this error

class PygameWorld(World):
    ''' A World which displays its objects as circles in a pygame display

        Supported display attributes:
                pos (2d array)
                radius
                color
                width
    '''
    import pygame as pyg
    def __init__(self, wh=(500, 500), argfuncs={}, fill=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self.argfuncs = {'pos': lambda o: np.array(o.pos[0:2], dtype='int'),
                         'color': lambda o: (255, 255, 255),
                         'radius': lambda o: 4,
                         'width' : lambda o: 0
                         }
        self.argfuncs.update(argfuncs)

        self.screen = self.pyg.display.set_mode(wh)
        self.frame = self.pyg.Surface(wh)
        self.trail = self.pyg.Surface(wh)

        self.fill = np.array(fill, dtype='int')
        self.frame.set_colorkey(self.fill)
        self.trail.set_colorkey(self.fill)

    def circle(self, color, pos, radius, width=0):
        ''' Pygame is a pain and doesn't allow the use of kwargs to fill in
        positional arguments (for no good reason!). I really like using this
        feature so I contrived a simple workaround. Whatever.
        '''
        self.pyg.draw.circle(self.frame, color, pos, radius, width)
        self.pyg.draw.circle(self.trail, color, pos, 0, width)

    def draw(self):
        ''' Draw all objects in self, update display '''
        self.screen.fill(self.fill)
        self.frame.fill(self.fill)

        for object in self.objects:
            kwargs = dict([(arg, f(object))
                           for arg, f in self.argfuncs.items()])

            self.circle(**kwargs)

        self.screen.blit(self.trail,(0,0))
        self.screen.blit(self.frame,(0,0))
        self.pyg.display.update()


class VWorld(World):
    ''' A World whose objects have Visual avatars '''
    import visual as v
    def __init__(self, wh=(500, 500), argfuncs={}, title="nthdemo Visual", **kwargs):
        super().__init__(**kwargs)
        self.argfuncs = {'pos': lambda o: np.array(o.pos[0:3]),
                         'color': lambda o: (255, 255, 255),
                         'radius': lambda o: 10,
                         'make_trail': lambda o: True
                         }
        self.argfuncs.update(argfuncs)
        self.screen = self.v.display(title=title, width=wh[0], height=wh[1])
        self.screen.center = self.size[0:3]/2
        self.avatars = {}

    def insert(self, *objs):
        for object in objs:
            self.objects.add(object)
            kwargs = dict([(arg, f(object))
                           for arg, f in self.argfuncs.items()])
            self.avatars[object] = self.v.sphere(**kwargs)

    def draw(self):
        for object in self.objects:
            kwargs = dict([(arg, f(object))
                           for arg, f in self.argfuncs.items()])
            #self.avatars[object].__dict__.update(kwargs)#IT DOESNT WORK BUT I WANT IT TO
            self.avatars[object].pos = kwargs['pos']
            self.avatars[object].color = kwargs['color']
            self.avatars[object].trail_object.color[-1] = kwargs['color']

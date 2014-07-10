from ndemo import *
import numpy as np


class Phobject(object):
    ''' A basic physics object. mass does nothing currently '''
    def __init__(self, pos=(0, 0, 0), vel=None, acc=None, mass=1):
        self.d = len(pos)
        self.pos = np.array(pos, dtype='float64')

        if vel:
            if len(vel) != self.d:
                raise ValueError("Velocity vector of wrong dimension")
            self.vel = np.array(vel, dtype='float64')
        else: self.vel = np.zeros(self.d, dtype='float64')

        if acc:
            if len(acc) != self.d:
                raise ValueError("Acceleration vector of wrong dimension")
            self.acc = np.array(acc, dtype='float64')
        else: self.acc = np.zeros(self.d, dtype='float64')

        self.m = mass

    def step(self, dt):
        #+= doesnt work
        #its because the arrays are ints... c based libraries stop meddling with my duck typing :(
        self.pos = self.pos + self.vel*dt
        self.vel = self.vel + self.acc*dt

    def get_heading(self, x):
        ''' Calculates a heading vector from the object to the target, where
        heading*dist = a vector in direction heading with magnitude dist
        '''
        # vector of the difference in positions
        diffvector = x - self.pos
        # find the magnitude of diffvector as coefmod
        coefmod = np.sqrt(np.sum(diffvector**2))
        # divide diffvector by this magnitude so that the magnitude of the
        # heading vector will be 1
        return diffvector/coefmod

    def get_dist(self, x):
        ''' Euclidean distance between self.pos and x '''
        return np.sqrt(np.sum((self.pos - x)**2))


# Newtonian Gravitation /-------------------------------------------
#-------------------------------------------------------------------

class NewtCage(World):
    ''' A World which supports Newtonian gravitation objects '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # objects can move, attractors can exert gravitational force; the lists
        # can overlap
        self.attractors = set()

    def world_step(self, dt):
        for object in self.objects:
            object.gravitate(self.attractors)
        super().world_step(dt)


class Newt(Phobject):
    ''' A particle that obeys Newtonian gravitation.
    the name is a play on turtle.
    i like it.
    '''
    def gravitate(self, attractors):
        ''' Calculate the net force from gravitation '''
        netF = np.zeros(self.d, dtype='float64')

        for at in attractors:
            if at is self: continue
            dist = self.get_dist(at.pos)
            # to be implemented: exponent scales with dim?, G?
            F = (self.m * at.m) / dist**2
            heading = self.get_heading(at.pos)

            netF += F*heading

        self.acc = netF/self.m


# Boids /-----------------------------------------------------------
#-------------------------------------------------------------------

class BoidCage(World):
    ''' A World that handles flocking for Boids '''
    def world_step(self, dt):
        for boid in self.objects:
            flock, jerks = boid.see(self.objects)
            if flock:
                boid.center(flock, dt)
                boid.copy(flock, dt)
            if jerks: boid.avoid(jerks, dt)
            self.constrain(boid, dt)
        super().world_step(dt)

    def constrain(self, boid, dt):
        ''' prevents boids from leaving the confines of the cage '''
        for i, p in enumerate(boid.pos):
            if p <= boid.avoidrange:
                boid.vel[i] += boid.avoidmag*dt
            elif self.size[i] - p <= boid.avoidrange:
                boid.vel[i] -= boid.avoidmag*dt


class Boid(Phobject):
    ''' A Boid (a naive solution)
    Rules:
        - avoid objects
        - steer towards center of flock
        - copy flockmates heading
    '''
    def __init__(self, avoid=200, center=0.1, copy=1,
                 avoidrange = 10, flockrange = 100, **kwargs):
        super().__init__(**kwargs)

        self.avoidmag = avoid
        self.centermag = center
        self.copyweight = copy
        self.avoidrange = avoidrange
        self.flockrange = flockrange

    def see(self, objects):
        flock = []
        jerks = []
        for object in objects:
            if object is self: continue
            dist = self.get_dist(object.pos)
            if dist <= self.flockrange: flock.append(object)
            if dist <= self.avoidmag: flock.append(object)
        return flock, jerks

    def avoid(self, objects, dt):
        posi = []
        weights = []
        for jerk in objects:
            posi.append(jerk.pos)
            weight = avoidrange - self.get_dist(jerk.pos)
            if weight < 0: weight = 0
        avoid_pos = np.average([pos*weight
                                for pos, weight in zip(posi, weights)])
        self.vel += -(self.get_heading(avoid_pos)*self.avoidmag)*dt

    def center(self, flock, dt):
        flock_pos = np.average([friend.pos for friend in flock])
        self.vel += self.get_heading(flock_pos)*self.centermag*dt

    def copy(self, flock, dt):
        flock_vel = np.average([friend.vel for friend in flock])
        self.vel = ((self.vel + (flock_vel*self.copyweight))/(self.copyweight+1))*dt


# Pathfinding (lol) /-----------------------------------------------
#-------------------------------------------------------------------

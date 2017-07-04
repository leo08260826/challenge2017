from model_const import *

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

class Barrier(object):
    def __init__(self, playerIndex, position, direction):
        self.playerIndex = playerIndex
        self.position = position
        self.direction = direction
        self.timer = barrierTimer

    def tickCheck(self):
        """
        If the barrier is active, update the timer and return True, otherwise return False.
        """
        if self.timer > 0:
            self.timer -= 1
            return True
        else:
            return False

    def bump(self, target):
        a = []
        b = []
        c = []
        d = []
        ba = []
        ca = []
        da = []
	    ac = []
        dc = []
        bc = []
        a.append(self.position[0] + 0.5 * barrierWidth * dirConst[(self.direction + 1) % 8 + 1][0])
        a.append(self.position[1] + 0.5 * barrierWidth * dirConst[(self.direction + 1) % 8 + 1][1])
        b.append(self.position[0] + 0.5 * barrierWidth * dirConst[(self.direction + 5) % 8 + 1][0])
        b.append(self.position[1] + 0.5 * barrierWidth * dirConst[(self.direction + 5) % 8 + 1][1])
        c.append(target.position[0])
        c.append(target.position[1])
        d.append(target.position[0] + dirConst[target.direction][0])
        d.append(target.position[1] + dirConst[target.direction][1])
        for i in range(2):
            ba.append(b[i] - a[i])
            ca.append(c[i] - a[i])
            da.append(d[i] - a[i])
            dc.append(d[i] - c[i])
            ac.append(a[i] - c[i])
            bc.append(b[i] - c[i])
        c1 = cross(ba, ca)
        c2 = cross(ba, da)
        c3 = cross(dc, ac)
        c4 = cross(dc, bc)
        if c1 * c2 < 0 and c3 * c4 < 0:
            return True
        else:
            return False

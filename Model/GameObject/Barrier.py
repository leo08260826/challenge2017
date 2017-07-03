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
		a = self.position + 0.5 * barrierWidth * dirConst[(self.direction + 2) % 9]
		b = self.position + 0.5 * barrierWidth * dirConst[(self.direction + 6) % 9]
		c = target.position
		d = target.position + dirConst[target.direction]
		c1 = cross(b - a, c - a)
		c2 = cross(b - a, d - a)
		c3 = cross(d - c, a - c)
		c4 = cross(d - c, b - c)
		if c1 * c2 < 0 and c3 * c4 < 0:
			return True
		else:
			return False

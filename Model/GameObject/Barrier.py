class Barrier(object):
	def __init__(self, playerIndex, position, direction, timer):
		self.playerIndex = playerIndex
		self.position = position
		self.direction = direction
		self.timer = timer

	def update():
		timer -= 1;

	def isActive():
		"""
		Check if the barrier is active, return true if active, false otherwise.
		"""
		if (self.timer > 0):
			return True
		else:
			return False




		
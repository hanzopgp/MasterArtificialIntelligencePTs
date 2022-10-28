from pyroborobo import Pyroborobo, Controller
import numpy as np
from random import random

def principal_value(deg):
    deg_mod = np.mod(deg, 360)
    if deg_mod > 180:
        return deg_mod - 360
    else:
        return deg_mod


def angle_diff(x, y):
    return principal_value(x - y)


class AttractionController(Controller):

	def __init__(self, world_model):
		# It is *mandatory* to call the super constructor before any other operation to
		# link the python object to its C++ counterpart
		Controller.__init__(self, world_model)
		self.rob = Pyroborobo.get()
		self.camera_max_range = 0
		self.repulse_radius = 0
		self.orientation_radius = 0

	def reset(self):
		self.repulse_radius = 0.2
		self.orientation_radius = 0.6

	def diff_angles(a,b):
		angle = (a+b) % 360
		return min( angle,180-angle )

	def sig(self, x):
 		return 1/(1 + np.exp(-x))

	def step(self):
		self.set_translation(1)
		self.set_rotation(0)
		distances = self.get_all_distances()

		epsilon = 1e-5 ## avoid dividing by zero
		avoid_factor = 5 ## if that value is high, agents avoid from a longer distance
		min_distance = 0.1
		for i in range(self.nb_sensors):
			is_robot = self.get_robot_id_at(i) != -1
			is_wall = self.get_wall_at(i)
			if is_wall:
				if (distances[1] < 1  # if we see something on our right
						or distances[2] < 1):  # or in front of us
					inverse_distance = 1/((distances[1]) + epsilon) * avoid_factor
					self.set_rotation(-self.sig(inverse_distance))  # turn left
				elif distances[3] < 1:  # Otherwise, if we see something on our left
					inverse_distance = 1/((distances[3]) + epsilon) * avoid_factor
					self.set_rotation(- self.sig(inverse_distance))  # turn right
			elif is_robot:
				tmp_dist = [d for d in distances if d != 1.] #On prend que les obstacles trouves
				if len(tmp_dist) > 0:
					nb = len(tmp_dist)
					poids = [(nb - i) for i in range(nb,-1,-1)]
					s = sum(poids)
					poids = [el/(s+epsilon) for el in poids]
					camera_angle_rad = self.get_all_sensor_angles()
					camera_angle = camera_angle_rad * 180 / np.pi
					nb_right = 0
					nb_left = 0
					nb_front = 0 
					nb_behind = 0
					turn_rate = 0
					rank = -1
					for i in np.argsort(tmp_dist):
						rank += 1
						angle = camera_angle[i]
						
						if angle == 0: #deja devant donc ok
							continue

						if angle > 0: #robot a droite
							turn_rate += 1 * poids[rank]
						else:         #robot a gauche
							turn_rate -= 1 * poids[rank]

					self.set_rotation(-turn_rate)

if __name__ == "__main__":
    rob = Pyroborobo.create("config/simple.properties",
                            controller_class=AttractionController)
    rob.start()
    rob.update(100000)
    rob.close()

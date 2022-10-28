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


	def sig(self, x):
		return 1/(1 + np.exp(-x))

	def ecart_angles(self,a,b):
		x = abs(360-a)
		y = abs(360-b)
		opt1 = abs(a-b)
		opt2 = 360-abs(a-b)
		mini = min( abs(a-b) , 360-abs(a-b))

		if x > y:
			return mini
		else:
			return -mini

	def step(self):
		self.set_translation(1)
		self.set_rotation(0)
		distances = self.get_all_distances()
		min_distance = 0.1
		epsilon = 1e-5
		avoid_factor = 3

		for i in range(self.nb_sensors):
			is_robot = self.get_robot_id_at(i) != -1
			is_wall = self.get_wall_at(i)
			if is_wall or (is_robot and distances.min() < min_distance):
				if (distances[1] < 1  # if we see something on our right
						or distances[2] < 1):  # or in front of us
					inverse_distance = 1/((distances[1]) + epsilon) * avoid_factor
					self.set_rotation(self.sig(inverse_distance))  # turn left
				elif distances[3] < 1:  # Otherwise, if we see something on our left
					inverse_distance = 1/((distances[3]) + epsilon) * avoid_factor
					self.set_rotation(- self.sig(inverse_distance))  # turn right

		my_hdg = self.absolute_orientation
		d = self.get_all_distances()
		is_wall_F = self.get_wall_at(2)
		is_wall_FR = self.get_wall_at(3)
		is_wall_FL = self.get_wall_at(1)
		if is_wall_F or is_wall_FR or is_wall_FL:
			if d[2] < 0.2 or d[1] < 0.3 :
				if random() < 0.5:
					self.set_rotation( random() )
				else:
					self.set_rotation( -random() )
			elif d[3] < 0.3:
				self.set_rotation(  - random() )
			return 0
		orientations = []
		for i in range(self.nb_sensors):
			is_robot = self.get_robot_id_at(i) != -1
			if is_robot:
				orient_angle = self.get_robot_relative_orientation_at(i)
				orientations.append( orient_angle )
		if orientations == []:
			return 0 
		orientations = np.degrees(orientations)
		mean = np.average(orientations)
		ecart = self.ecart_angles(my_hdg,mean)
		if ecart > 0:
			self.set_rotation( np.radians(abs(ecart))  * 3/4 )
		else:
			self.set_rotation( -np.radians(abs(ecart)) * 3/4 )






if __name__ == "__main__":
    rob = Pyroborobo.create("config/simple.properties",
                            controller_class=AttractionController)
    rob.start()
    rob.update(100000)
    rob.close()

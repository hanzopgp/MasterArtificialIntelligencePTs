from pyroborobo import Pyroborobo, Controller
import numpy as np


class TutorialController(Controller):
	robot_index_offset = 1048576

	def __init__(self, world_model):
		# It is *mandatory* to call the super constructor before any other operation to link the python object to its C++ counterpart
		Controller.__init__(self, world_model)
		self.rob = Pyroborobo.get()
		print("I'm a Python controller")

	def reset(self):
		print("I'm initialised")

	def sig(self, x):
 		return 1/(1 + np.exp(-x))

	def get_discrete_value(self, x):
		return np.clip((x*0.5) - 1, -1, 1)

	def step(self):  # step is called at each time step
		# Simple avoidance
		self.set_translation(1)  # Let's go forward
		self.set_rotation(0)
		# Now, our world_model object is a PyWorldModel, we can have access to camera_* properties
		camera_dist = self.get_all_distances()



		## after checking the simulatiuon, there is 8 sensor :
			## 0 --> left       
			## 1 --> front-left  
			## 2 --> front
			## 3 --> front-right
			## 4 --> right
			## 5 --> back-right
			## 6 --> back
			## 7 --> back-left
		## if we divide the [-1, 1] rotation space by 8 we get discrete value
		## like -1, -0.75...0.75, 1
		## if we want our robots to collide and become a cluster we need to check 
		## where is the closest robots and move towards it thanks to the rotation
		for i in range(self.nb_sensors):
			is_robot = self.get_robot_id_at(i) != -1
			is_wall = self.get_wall_at(i)
			## here we make clusters of robots
			if is_robot:
				min_side = camera_dist.argmin()
				min_value = camera_dist.min()
				if min_value != 1: ## check min_value to avoid perma rotating behavior
					if min_side < 5:
						self.set_rotation(self.get_discrete_value(min_side))
					## this is not really needed but the clustering is a bit faster
					else:
						if min_side == 5 or min_side == 6:
							self.set_rotation(1)
						else:
							self.set_rotation(-1)
			## here we just avoid walls depending the distance	
			elif is_wall:
				epsilon = 1e-5 ## avoid dividing by zero
				avoid_factor = 5 ## if that value is high, agents avoid from a longer distance
				if (camera_dist[1] < 1  # if we see something on our right
						or camera_dist[2] < 1):  # or in front of us
					inverse_distance = 1/((camera_dist[1]) + epsilon) * avoid_factor
					self.set_rotation(self.sig(inverse_distance))  # turn left
				elif camera_dist[3] < 1:  # Otherwise, if we see something on our left
					inverse_distance = 1/((camera_dist[3]) + epsilon) * avoid_factor
					self.set_rotation(- self.sig(inverse_distance))  # turn right



		# # now let's get talkative
		# if self.id == 0:
		#     print(f"I am {self}, {self.id}, at position {self.absolute_position} and orientation {self.absolute_orientation}")
		#     for i in range(self.nb_sensors):
		#         print(f"Sensor {i}:")
		#         print(f"\tdist: {self.get_distance_at(i)}")
		#         print(f"\tis object: {self.get_object_at(i) != -1}")
		#         print(f"\tis_wall: {self.get_wall_at(i)}")
		#         print(f"\tis robot: {self.get_robot_id_at(i) != -1}")
		#         is_robot = self.get_robot_id_at(i) != -1
		#         is_wall = self.get_wall_at(i)
		#         if is_robot:
		#             robid = self.get_robot_id_at(i)
		#             print(f"\trobot id: {robid}")
		#             print(f"\trobot's controller: {self.get_robot_controller_at(i)}")
		#             ctl = self.get_robot_controller_at(i)
		#             print(f"\tThis robot is at {ctl.absolute_position} with orientation {ctl.absolute_orientation}.")
		#         elif self.get_object_at(i) != -1:  # then it's an object
		#             print(f"\tphysical object instance: {self.get_object_instance_at(i)}")


if __name__ == "__main__":
    rob = Pyroborobo.create("config/simple.properties",
                            controller_class=TutorialController)
    rob.start()
    rob.update(10000)
    rob.close()
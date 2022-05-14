from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random


class RoomEnv():

    def __init__(self, temp_low=20, temp_up=23, x_dim=10, y_dim=10, z_dim=3):
        ''' This Methode is to initialize parameters for the room.
            
            - temp_low: sets the lower comfort temperature
            - temp_up: Seths the upper comfort temperature
            - x_dim: Room length
            - y_dim: Room width
            - z_dim: Room hight
        '''
        self.action_space = Discrete(5)
        self.observation_space = Box(low=np.array([0]), high=np.array([100]))
        self.temp_low = temp_low
        self.temp_up = temp_up
        self.state = ((temp_low + temp_up) / 2) + random.randint(-3,3)
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        self.room_volume = x_dim * y_dim * z_dim
        self.episode_lenth = 100 # Placeholder must be defined later
        self.heat_ransf_coef = 

    @staticmethod
    def heat_exchange(x, y):
        return x+y

    def step(self):
        self.heat_exchange(2,3)
        pass

    def render(self):
        pass

    def reset(self):
        pass


env = RoomEnv()
print(env.step())
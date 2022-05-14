from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random

'''
[1]: H. Zhao, J. Zhao, T. Shu, and Z. Pan, “Hybrid-Model-Based Deep Reinforcement Learning for Heating, Ventilation, and Air-Conditioning Control,” Frontiers in Energy Research, vol. 8, 2021, doi: 10.3389/fenrg.2020.610518.
'''


class RoomEnv():

    def __init__(self, temp_low=20, temp_up=23, x_dim=5, y_dim=5, z_dim=5):
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
        self.episode_lenth = 100 # TODO: Placeholder - must be defined later
        self.heat_trans_coef = 0.4 # TODO: Placeholder - Further research
        self.heat_of_air = 1.005 # [1]

    @staticmethod
    def roc_heat_in_walls(heat_trans_coef, x_dim, y_dim, z_dim, ambient_temp, zone_temp):
        ''' This methode calculates the rate of heat change in the walls. It is assumed, that all walls (excluding the floor) have the same values [1]. '''
        area_a = x_dim * z_dim * 2
        area_b = y_dim * z_dim * 2
        area_c = x_dim * y_dim * 1
        total_area = area_a + area_b + area_c
        Hwzt = heat_trans_coef * total_area * (ambient_temp - zone_temp)
        return Hwzt

    @staticmethod
    def zone_temp(delta_t, Hwzt, Hhzt, room_volume, air_density, air_heat):
        

    def step(self):
        Hwzt = self.rate_heat_exchange(self.heat_trans_coef, self.x_dim, self.y_dim, self.z_dim, 0, 20)
        print(Hwzt)
        pass

    def render(self):
        pass

    def reset(self):
        pass


env = RoomEnv()
print(env.step())
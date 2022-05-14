from ctypes.wintypes import HHOOK
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random

'''
[1]: H. Zhao, J. Zhao, T. Shu, and Z. Pan, “Hybrid-Model-Based Deep Reinforcement Learning for Heating, Ventilation, and Air-Conditioning Control,” Frontiers in Energy Research, vol. 8, 2021, doi: 10.3389/fenrg.2020.610518.
[2]: Engineering ToolBox, (2008). Radiators - Heat Emission. [online] Available at: https://www.engineeringtoolbox.com/heat-emission-radiators-d_1121.html [Accessed 14 May 2022].
'''


class RoomEnv():

    def __init__(self, temp_low=19, temp_up=25, x_dim=5, y_dim=5, z_dim=5):
        ''' This Methode is to initialize parameters for the room.
            
            - temp_low: sets the lower comfort temperature in C°
            - temp_up: Seths the upper comfort temperature in C°
            - x_dim: Room length in meter
            - y_dim: Room width in meter
            - z_dim: Room hight in meter
        '''
        self.action_space = Discrete(5)
        self.observation_space = Box(low=np.array([0]), high=np.array([100]))
        self.temp_low = temp_low
        self.temp_up = temp_up
        self.state = ((temp_low + temp_up) / 2) + random.randint(-3,3)
        self.x_dim = x_dim # in meter
        self.y_dim = y_dim # in meter
        self.z_dim = z_dim # in meter
        self.room_volume = x_dim * y_dim * z_dim
        self.episode_lenth = 100 # TODO: Placeholder - must be defined later
        self.heat_trans_coef = 0.003 # in kW/m^2C° [1]
        self.heat_of_air = 1.005 # kJ/kgC° [1]
        self.air_density = 1.25 # kg/m^3 [1]
        self.delta_t = 1 # in seconds [1]
        self.radiator_length = 1 # in meter [2]
        self.radiator_hight = 0.5 # in meter [2]

    @staticmethod
    def roc_heat_in_walls(heat_trans_coef, x_dim, y_dim, z_dim, ambient_temp, zone_temp):
        ''' This method calculates the rate of heat change in the walls. It is assumed, that all walls (excluding the floor) have the same values [1]. '''
        area_a = x_dim * z_dim * 2
        area_b = y_dim * z_dim * 2
        area_c = x_dim * y_dim * 1
        total_area = area_a + area_b + area_c
        Hwzt = heat_trans_coef * total_area * (ambient_temp - zone_temp)
        return Hwzt

    @staticmethod
    def roc_heat_in_zone(action, radiator_lenght, radiator_hight):
        ''' This method calculates the rate of heat change in the zone. The value gets multiplied by the ctrl_value. This variable is defined by
            the choosen action divided by 5, which is the maximum value on a common thermostatic valve [2]. '''
        ctrl_value = action / 5
        Hhzt = ctrl_value * (41 * 4.9 * radiator_lenght * (1 + 8 * radiator_hight))
        return Hhzt

    @staticmethod
    def zone_temp(delta_t, Hwzt, Hhzt, room_volume, air_density, heat_of_air):
        ''' This method calculates the temperature difference between t and t+1 in the zone [1]. '''
        delta_temp = delta_t * (Hwzt + Hhzt) / room_volume * air_density * heat_of_air
        return delta_temp

    def step(self):
        Hwzt = self.roc_heat_in_walls(self.heat_trans_coef, self.x_dim, self.y_dim, self.z_dim, 0, 20)
        Hhzt = self.roc_heat_in_zone(5, self.radiator_length, self.radiator_hight)
        delta_temp = self.zone_temp(self.delta_t, Hwzt, Hhzt, self.room_volume, self.air_density, self.heat_of_air)
        print(Hhzt)
        pass

    def render(self):
        pass

    def reset(self):
        pass


env = RoomEnv()
env.step()
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import random


'''
[1]: H. Zhao, J. Zhao, T. Shu, and Z. Pan, “Hybrid-Model-Based Deep Reinforcement Learning for Heating, Ventilation, and Air-Conditioning Control,” Frontiers in Energy Research, vol. 8, 2021, doi: 10.3389/fenrg.2020.610518.
[2]: Engineering ToolBox, (2008). Radiators - Heat Emission. [online] Available at: https://www.engineeringtoolbox.com/heat-emission-radiators-d_1121.html [Accessed 14 May 2022].
[3]: https://www.youtube.com/watch?v=bD6V3rcr_54
[4]: https://www.scplumbing.co.uk/helpful-info/how-quickly-should-radiators-heat-up
[5]: https://www.castrads.com/uk/resources/calculators/panel-radiator-outputs/
'''



class Radiator():
    '''
        This class represents everything related to the radiator. Initially, the
        radiator has a hight and lenth. It is assumed, that this is a typical radiator 
        which heats up within 40 minutes at maximum level (5) [4]. Furthermore, to
        keep it simple, the radiator shows a linear behaviour in heating up and 
        cooling down. 
    '''

    def __init__(self, length=1, hight=0.5):
        self.radiator_length = length # in meter [2]
        self.radiator_hight = hight # in meter [2]
        self.state = 0 # Continuous, between 0 and 1

    def give(self, radiator_lenght, radiator_hight):
        ''' This method calculates the rate of heat change in the zone. The value gets multiplied 
            by the ctrl_value. This variable is defined by the choosen action divided by 5, which 
            is the maximum value on a common thermostatic valve [2]. '''
        give = self.state * (41 * 3.1 * radiator_lenght * (1 + 8 * radiator_hight))
        return give

    def set_state(self, action):
        ''' Method that returns the current state of the radiator. The return value is 
            continuous between 0 and 1. This means that with the value 1 the radiator 
            reached its maximum power. '''
        if action != 0:
            self.state += action/5 * 0.0416667 # 0.0416667 is the gain per second at the highest level (5)
            if self.state >= 1:
                self.state = 1
        else:
            self.state += (-3/5) * 0.0416667 # -3 is an assumption
            if self.state <= 0:
                self.state = 0



class RoomEnv():
    '''
        This class represents the environment in which the agent will train.
        It is built up on the YouTube tutorial Building a Custom Environment for 
        Deep Reinforcement Learning with OpenAI Gym and Python by Nicholas Renotte [3].
    '''

    def __init__(self, temp_low=19, temp_up=25, x_dim=20, y_dim=10, z_dim=10):
        ''' This Methode is to initialize parameters for the room.
            
            - temp_low: sets the lower comfort temperature in C°
            - temp_up: Seths the upper comfort temperature in C°
            - x_dim: Room length in meter
            - y_dim: Room width in meter
            - z_dim: Room hight in meter
        '''
        self.action_space = Discrete(6)
        self.observation_space = Box(low=np.array([0]), high=np.array([100]))
        self.temp_low = temp_low
        self.temp_up = temp_up
        self.state = ((self.temp_low + self.temp_up) / 2) + random.randint(-3,3)
        self.x_dim = x_dim # in meter
        self.y_dim = y_dim # in meter
        self.z_dim = z_dim # in meter
        self.room_volume = x_dim * y_dim * z_dim
        self.sim_duration = 100 # TODO: Placeholder - must be defined later
        self.heat_trans_coef = 0.001 # in kW/m^2C° [1]
        self.heat_of_air = 1.005 # kJ/kgC° [1]
        self.air_density = 1.25 # kg/m^3 [1]
        self.delta_t = 1 # in seconds [1]


    def take():
        # receives heat
        pass

    @staticmethod
    def take(heat_trans_coef, x_dim, y_dim, z_dim, ambient_temp, zone_temp):
        ''' This method calculates the rate of heat change in the walls. It is assumed, 
            that all walls (excluding the floor) have the same values [1]. '''
        area_a = x_dim * z_dim * 2
        area_b = y_dim * z_dim * 2
        area_c = x_dim * y_dim * 1
        total_area = area_a + area_b + area_c
        take = heat_trans_coef * total_area * (ambient_temp - zone_temp)
        return take


    @staticmethod
    def cal_delta_temp(delta_t, Hwzt, Hhzt, room_volume, air_density, heat_of_air):
        ''' This method calculates the temperature difference between t and t+1 in the zone [1]. '''
        delta_temp = delta_t * (Hwzt + Hhzt) / room_volume * air_density * heat_of_air
        return delta_temp

    def step(self):
        ''' Given an action, this method performs the change in the environment and returns state, reward, done and info. '''
        room_take = self.take(self.heat_trans_coef, self.x_dim, self.y_dim, self.z_dim, 0, 20)
        rad_give = raditator.give(raditator.radiator_length, raditator.radiator_hight)
        delta_temp = self.cal_delta_temp(self.delta_t, room_take, rad_give, self.room_volume, self.air_density, self.heat_of_air)
        self.state += delta_temp
        return self.state

    def render(self):
        pass

    def reset(self):
        ''' Resets the environment to start a new episode. '''
        self.state = ((self.temp_low + self.temp_up) / 2) + random.randint(-3,3)
        self.sim_duration = 100 # TODO: Placeholder - must be defined later

room = RoomEnv()
raditator = Radiator()

episode = 1
for episode in range(1,episode+1):
    state = room.reset()
    done = False
    score = 0
    time_step = 0
    print(state)

    while not done:
        if time_step % 60 == 0:
            action = room.action_space.sample()
            raditator.set_state(action)
            print("action: ", action, "state: ", room.step(), "rad_statee: ", raditator.state)
            #n_state, reward, done, info = env.step(action)
        else:
            raditator.set_state(action)
            print("action: ", action, "state: ", room.step(), "rad_state: ", raditator.state)
            #n_state, reward, done, info = env.step(action)
        #room.influences(raditator)
        #score+=reward
        time_step += 1
        #room.step()
        #raditator.update()
        #window.update()

        # For debugging
        if time_step == 1000:
            done = True
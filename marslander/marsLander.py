import sys
import math
import numpy as np

TEST_INPUT = False
TEST_IN_GAME = True
GAME_ZONE = {
    'x': 6999,
    'y': 2999
}
LANDING_ZONE_LENGTH = 1000
GRAVITY = 3.711
MAX_VERTICAL_SPEED = 40
MAX_HORIZONTAL_SPEED = 20
V_SPEED_TO_MAINTAIN = 21.9


class MarsLander:

    def __init__(self, surfaces_, landing_zone_):
        self.surfaces = surfaces_
        self.landing_zone = landing_zone_
        self.action = \
            {
                'angle': 0,
                'power': 0
            }
        self.x = []
        self.y = []
        self.h_speed = None
        self.v_speed = None
        self.fuel = None
        self.angle = None
        self.power = 0
        self.next_power = 0
        self.next_fuel = None
        self.next_angle = None
        self.next_x = None
        self.next_y = None
        self.next_h_speed = None
        self.next_v_speed = None

    def set_x_list(self, x):
        if len(self.x) < 2:
            self.x.append(x)
        else:
            self.x = self.x[1:]
            self.x.append(x)

    def set_y_list(self, y):
        if len(self.y) < 2:
            self.y.append(y)
        else:
            self.y = self.y[1:]
            self.y.append(y)

    def set_next_power(self, next_power_):
        if next_power_ > self.power:
            self.next_power += 1
        elif next_power_ < self.power:
            self.next_power -= 1

    def set_next_angle(self, next_angle_):
        self.next_angle = self.angle + next_angle_

    def set_next_fuel(self):
        self.next_fuel = self.fuel - self.next_power

    def set_next_x(self):
        if len(self.x) == 2:
            self.next_x = 2 * self.x[1] - self.x[0] - self.next_power \
                          * math.sin(math.radians(self.next_angle))

    def set_next_y(self):
        if len(self.y) == 2:
            self.next_y = 2 * self.y[1] - self.y[0] - GRAVITY + self.next_power \
                          * math.cos(math.radians(self.next_angle))

    def set_next_h_speed(self):
        self.next_h_speed = self.h_speed - self.next_power \
                            * math.sin(math.radians(self.next_angle))

    def set_next_v_speed(self):
        self.next_v_speed = self.v_speed - GRAVITY + self.next_power \
                            * math.cos(math.radians(self.next_angle))

    def get_current_surface_height(self):
        # above landing_zone
        if self.landing_zone['start'] <= self.x[1] <= self.landing_zone['end']:
            return {
                'y': landing_zone['start_height'],
                'landing_zone': True
            }
        else:
            for surface in self.surfaces:
                if surface['start'] <= self.x[1] <= surface['end']:
                    return {
                        'y': surface['tangent'] * self.x[1] + surface['start_height'],
                        'landing_zone': False
                    }

    def update_lander(self, lander_):
        self.set_x_list(lander_['x'])
        self.set_y_list(lander_['y'])
        self.h_speed = lander_['h_speed']
        self.v_speed = lander_['v_speed']
        self.fuel = lander_['fuel']
        self.angle = lander_['angle']
        self.power = lander_['power']

    def update_action(self, action_):
        self.set_next_power(action_['power'])
        self.set_next_fuel()
        self.set_next_angle(action_['angle'])
        self.set_next_x()
        self.set_next_y()
        self.set_next_h_speed()
        self.set_next_v_speed()


def get_data():
    surface_n = int(input())  # the number of points used to draw the surface of Mars.
    results = []

    for i in range(surface_n):
        # land_x: X coordinate of a surface point. (0 to 6999)
        # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
        land_x, land_y = [int(j) for j in input().split()]

        surface_ = {
            'x': land_x,
            'y': land_y
        }
        results.append(surface_)

    return results


def get_surfaces(surfaces_data_):
    landing_results = []
    for i in range(len(surfaces_data_) - 1):
        landing_result = \
            {'start': surfaces_data_[i]['x'],
             'end': surfaces_data_[i + 1]['x'],
             'start_height': surfaces_data_[i]['y'],
             'end_height': surfaces_data_[i + 1]['y']
             }

        landing_result['x'] = landing_result['end'] - landing_result['start']
        landing_result['y'] = landing_result['end_height'] - landing_result['start_height']
        landing_result['tangent'] = landing_result['y'] / landing_result['x']

        landing_results.append(landing_result)

    return landing_results


def get_landing_zone(surfaces_):
    for surface in surfaces_:
        if surface['x'] >= LANDING_ZONE_LENGTH and surface['tangent'] == 0:
            return surface


def get_mars_lander_data():
    data = [int(i) for i in input().split()]

    lander_ = \
        {
            'x': data[0],
            'y': data[1],
            'h_speed': data[2],
            'v_speed': data[3],
            'fuel': data[4],
            'angle': data[5],
            'power': data[6]
        }

    return lander_


surfaces_data = get_data()

# if TEST_INPUT:
#     print(f'surfaces_data: {surfaces_data}', file=sys.stderr, flush=True)

surfaces = get_surfaces(surfaces_data)

# if TEST_INPUT:
#     print(f'surfaces: {surfaces}', file=sys.stderr, flush=True)

landing_zone = get_landing_zone(surfaces)

# if TEST_INPUT:
#     print(f'flat_ground: {landing_zone}', file=sys.stderr, flush=True)

mars_lander = MarsLander(surfaces, landing_zone)

round_ = 0
next_angle = 0
next_power = 4

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # angle: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).

    if round_ > 0:
        print(f'round: {round_}', file=sys.stderr, flush=True)

    lander = get_mars_lander_data()

    mars_lander.update_lander(lander)

    if TEST_INPUT:
        print(f'lander: {lander}', file=sys.stderr, flush=True)

    action = {
        'angle': next_angle,
        'power': next_power
    }

    mars_lander.update_action(action)

    if round_ >= 2:
        print(f'action', file=sys.stderr, flush=True)
        current_surface = mars_lander.get_current_surface_height()
        if current_surface['landing_zone']:
            if abs(mars_lander.next_h_speed) <= MAX_HORIZONTAL_SPEED:
                next_angle = 0
                if abs(mars_lander.next_v_speed) <= MAX_VERTICAL_SPEED:
                    next_power = 0
                else:
                    next_power = 4
            else:
                pass

    if TEST_IN_GAME and round_ >= 2:
        print(
            f"x: {mars_lander.x[1]} y: {mars_lander.y[1]} h_speed: {mars_lander.h_speed} v_speed: {mars_lander.v_speed}",
            file=sys.stderr, flush=True)
        print(f"fuel: {mars_lander.fuel} angle: {mars_lander.angle} power: {mars_lander.power}",
              file=sys.stderr, flush=True)
        current_surface = mars_lander.get_current_surface_height()
        print(f"surface: {current_surface['y']} landing_zone: {current_surface['landing_zone']}",
              file=sys.stderr, flush=True)

        print(f'\n',
              file=sys.stderr, flush=True)

        print(
            f"next_x: {mars_lander.next_x} next_y: {mars_lander.next_y} next_h_speed: {mars_lander.next_h_speed} next_v_speed: {mars_lander.next_v_speed}",
            file=sys.stderr, flush=True)
        print(
            f"next_fuel: {mars_lander.next_fuel} next_angle: {mars_lander.next_angle} next_power: {mars_lander.next_power}",
            file=sys.stderr, flush=True)

    # 2 integers: rotate power. rotate is the desired rotation angle (should be 0 for level 1), power is the desired thrust power (0 to 4).
    print(f"{action['angle']} {action['power']}")

    round_ += 1

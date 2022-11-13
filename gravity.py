import random
import datetime
import pygame
import time
import math

weght, heght = 1200, 800
pygame.init()
screen = pygame.display.set_mode((weght, heght))
RED = (225, 0, 0)
BLACK = (0, 0, 0)
timer = 0
mass_point = []  # pos_x,pos_y, deltaV_x, deltaV_y, mass
delta_time = 0.01
max_mass = 0
super_nova_list = []
g_const = 0.1


def get_pos_delta(pos_d, pos_up):
    """подсчитываем разницу координат и длину вектора"""
    radius = round(((-pos_d[0] + pos_up[0]) ** 2 + (-pos_d[1] + pos_up[1]) ** 2) ** 0.5, 4)

    return (-pos_d[0] + pos_up[0], -pos_d[1] + pos_up[1], radius)


def max_mass_target(point):
    target = [((-20, 0), (20, 0)),
              ((0, -20), (0, 20))]

    for item in target:
        pygame.draw.line(screen, (100, 100, 100), point[0] + item[0][0], point[0] + item[1][0])


def update_pos(point):
    abc_x, abc_y = point[0]
    if abc_x > weght - 5 or abc_x <= 5:
        point[1] = -1 * point[1] * 0.9
        if point[3] == max_mass:
            point[2] = point[2] * 0.4
            point[1] = point[1] * 0.4
            # point[3] = point[3] * 1
        return (point[0][0] + point[1] / 0.4 + math.copysign(point[1], 2 * point[1]), point[0][1])
    if abc_y > heght - 5 or abc_y <= 5:
        point[2] = -1 * point[2] * 0.9
        if point[3] == max_mass:
            point[2] = point[2] * 0.4
            point[1] = point[1] * 0.4
        return (point[0][0], point[0][1] + point[2] / 0.4 + math.copysign(point[2], 2 * point[2]))
    return (point[0][0] + point[1], point[0][1] + point[2])


def collapse_area(point):
    if point[0][0] > weght * 0.15 and point[0][0] < weght * 0.85:
        if point[0][1] > heght * 0.15 and point[0][1] < heght * 0.85:
            return True
    return False


def color_point_mass(mass):
    global max_mass
    for point in mass:
        if point[3] > max_mass:
            max_mass = point[3]


def update_speed(mass_point, cur_point):
    a_x, a_y = 0, 0
    global super_nova_list

    def leght_r(pos_0, pos_i):
        return round(((pos_0[0] - pos_i[0]) ** 2 + (pos_0[1] - pos_i[1]) ** 2) ** 0.5, 0)

    for point in mass_point:
        if point != cur_point:
            ## d_x, d_y, r
            d_x, d_y, radius = get_pos_delta(cur_point[0], point[0])
            if radius == 0:
                continue
            # f_x, f_y
            if radius <= 4:
                if collapse_area(point):
                    if cur_point[3] > point[3]:
                        cur_point[3] += point[3]
                        # cur_point[1], cur_point[2] = 0, 0
                        super_nova_list.append(point[0])
                        pygame.draw.circle(screen, (255, 255, 255), point[0], 30, 1)
                        # time.sleep(0.1)
                        pygame.draw.circle(screen, (0, 0, 0), point[0], 10, 10)
                        mass_point.remove(point)
                        # pygame.draw.circle(screen, (0,0,0), point[0], 30, 5)
                        color_point_mass(mass_point)
                        continue
                    else:
                        point[3] += cur_point[3]
                        pygame.draw.circle(screen, (255, 255, 255), point[0], 30, 1)
                        super_nova_list.append(point[0])
                        pygame.draw.circle(screen, (0, 0, 0), point[0], 10, 10)
                        mass_point.remove(cur_point)
                        color_point_mass(mass_point)
                        return 0, 0
            if len(super_nova_list) > 15:
                pygame.draw.circle(screen, (0, 0, 0), super_nova_list[0], 30, 1)
                super_nova_list = super_nova_list[1:]

            Force = point[3] * cur_point[3] * g_const / (radius ** 2)
            f_x, f_y = Force * d_x / radius, Force * d_y / radius
            a_x += f_x / cur_point[3]
            a_y += f_y / cur_point[3]
            # v-x, v-y

    return a_x * delta_time, a_y * delta_time


sleep_u = 0
while True:
    pygame.time.delay(30)
    # timer += 0.2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos_up = pygame.mouse.get_pos()
            mass_p = 1000 + round(19000 * random.random(), 2)
            speed_x, speed_y = get_pos_delta(pos_d, pos_up)[:2]
            mass_point.append([pos_d, speed_x * 0.001, speed_y * 0.001, mass_p])
            color_point_mass(mass_point)
            # pygame.draw.line(screen, (100, 250, 100), pos_d, pos_up, 2)
            print(len(mass_point),mass_point)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_d = pygame.mouse.get_pos()
            pygame.draw.circle(screen, RED, pos_d, 5, 5)
    if len(mass_point) > 0:
        for point in mass_point:
            pygame.draw.circle(screen, BLACK, point[0], 5, 5)
            point[0] = update_pos(point)

            if point[3] != max_mass:
                pygame.draw.circle(screen, (2, 100 + 140 * point[3] / max_mass, 12), point[0], 5, 5)
            else:
                pygame.draw.circle(screen, (0, 0, 255), point[0], 5, 5)
                # max_mass_target(point)
    if len(mass_point) > 1:
        for point in mass_point:
            dx, dy = update_speed(mass_point, point)
            point[1] += dx
            point[2] += dy

    pygame.display.update()

exit()

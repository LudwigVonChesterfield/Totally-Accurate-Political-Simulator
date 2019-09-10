"""
THIS MODULE HAS BEEN MADE BY LUDUK AT ningawent@gmail.com
PLEASE CONTACT BEFORE DISTRIBUTING AND OR MODIFYING THIS ON YOUR OWN ACCORD.

I, LUDUK, TAKE NO RESPONSIBILITY FOR ANY MISUES OF THIS MODULE.

also if you don't credit me you're a big meanie

!!!DISCLAIMER!!!
ALL INFORMATION CONTAINED IN THIS FILE HAS NOTHING TO DO WITH REAL LIFE.
ALL CHARACTERS DESCRIBED HERE ARE FICTIONARY.
ANY AND ALL SIMILARITIES ARE COMPLETELY COINCIDENTAL.
"""

import time
import math
import random

from graphics import *
from ideologies_game import IDEOLOGIES_CLASSIFICATION
from characters_presets import PRESET_CITIZENS

def clear(win):
    for item in win.items[:]:
        item.undraw()
    win.update()

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def get_closest_ideology(political_axis):
    closest_approximations = {}
    for ideology_name, ideology_axis in IDEOLOGIES_CLASSIFICATION.items():
        distance = 0
        for axis in ideology_axis["Axis"]:
            distance += (political_axis[axis] - ideology_axis["Axis"][axis]) ** 2
        distance = str(round(math.sqrt(distance), 1))
        if(distance in closest_approximations):
            closest_approximations[distance].append(ideology_name)
        else:
            closest_approximations[distance] = [ideology_name]
    return random.choice(closest_approximations[min(closest_approximations.keys(), key=float)])

def get_points_from_political_axis(political_axis):
    points = {}
    axises = political_axis.keys()
    i = 0
    for axis in axises:
        dist = translate(political_axis[axis], -100, 100, -width / 3, width / 3)

        radians = axis_radians[i]

        pt = Point((width / 2) + dist * math.sin(radians), (width / 2) + dist * math.cos(radians))

        if(dist > 0):
            points[i] = pt
        elif(dist < 0):
            points[(i + int(axis_count / 2))] = pt
        i += 1

    return points

def get_points_from_input():
    points = {}
    for axis in range(int(axis_count / 2)):
        dist = translate(int(input()), -100, 100, -width / 3, width / 3)

        radians = axis_radians[axis]

        pt = Point((width / 2) + dist * math.sin(radians), (width / 2) + dist * math.cos(radians))

        if(dist > 0):
            points[axis] = pt
        elif(dist < 0):
            points[(axis + int(axis_count / 2))] = pt

    return points
    

width = 700

win = GraphWin("Wind Hedgehog", width, width)

axis_count = 12
axis_radians = {}

axis_points = []
axis_names = [
    "Liberty",
    "Pacifism",
    "Materialism",
    "Individualism",
    "Reformism",
    "Industrialism",
    "Authority",
    "Militarism",
    "Spiritualism",
    "Collectivism",
    "Revolutionism",
    "Primitivism"
    ]

pt_center = Point(width / 2, width / 2)

rads_increment = math.radians(360 / axis_count)

def draw_background():
    radians = 0

    cir = Circle(pt_center, width / 3)
    cir.draw(win)

    for axis in range(axis_count):
        radians += rads_increment

        pt1 = pt_center
        pt2 = Point((width / 2) + (width / 3) * math.sin(radians), (width / 2) + (width / 3) * math.cos(radians))

        line = Line(pt1, pt2)
        line.draw(win)

        text = Text(pt2, axis_names[axis])
        text.setTextColor('red')
        text.setStyle('bold')
        text.draw(win)

        axis_radians[axis] = radians

def draw_political_hedgehog(points, line_color='blue', dot_color='red', dot_radius=5):
    keys = sorted(points.keys())

    for i in range(len(keys)):
        pt1 = points[keys[i]]
        pt2 = points[keys[(i + 1) % (len(keys))]]

        cir = Circle(pt1, dot_radius)
        cir.setFill(dot_color)
        cir.draw(win)

        line = Line(pt1, pt2)
        line.setWidth(3)
        line.setFill(line_color)
        line.draw(win) 

def draw_ideologies():
    for ideology_name, ideology_params in IDEOLOGIES_CLASSIFICATION.items():
        clear(win)
        draw_background()

        ideology_text = Text(Point(width / 2, 40), ideology_name)
        ideology_text.setTextColor('blue')
        ideology_text.setStyle('bold')
        ideology_text.draw(win)

        points = get_points_from_political_axis(ideology_params["Axis"])
        draw_political_hedgehog(points, line_color='blue', dot_color='red', dot_radius=5)
        time.sleep(2)
        pause = input()

def draw_users_and_their_ideologies():
    for user_name, user_params in PRESET_CITIZENS.items():
        clear(win)
        draw_background()

        political_axis = {}

        for element, sub_element in user_params["Axis"].items():
            if(type(sub_element) is dict):
                for sub_sub_element in element:
                    political_axis[element] = user_params["Axis"][element]["Value"]

        ideology_name = get_closest_ideology(political_axis)

        user_text = Text(Point(width / 2, 40), user_name)
        user_text.setTextColor('green')
        user_text.setStyle('bold')
        user_text.draw(win)

        ideology_text = Text(Point(width / 2, 80), "(" + ideology_name + ")")
        ideology_text.setTextColor('blue')
        ideology_text.setStyle('bold')
        ideology_text.draw(win)

        points = get_points_from_political_axis(political_axis)
        draw_political_hedgehog(points, line_color='green', dot_color='red', dot_radius=5)

        points = get_points_from_political_axis(IDEOLOGIES_CLASSIFICATION[ideology_name]["Axis"])
        draw_political_hedgehog(points, line_color='blue', dot_color='yellow', dot_radius=5)

        pause = input()
        time.sleep(2)

draw_background()
w = input()
# draw_ideologies()
draw_users_and_their_ideologies()

import math

import global_vars as gv

from .ideology import *
from .ideo_modificator import *

from .defines import *

def get_all_subclasses(cls):
  all_subclasses = []

  for subclass in cls.__subclasses__():
    all_subclasses.append(subclass)
    all_subclasses.extend(get_all_subclasses(subclass))

  return all_subclasses

def populate_ideologies(viewpoints):
  for ideology in get_all_subclasses(Ideology):
    gv.IDEOLOGIES[ideology.name] = ideology(viewpoints)

def populate_ideo_mods(viewpoints):
  for ideo_mod in get_all_subclasses(Ideo_Modifier):
    gv.IDE_MODS[ideo_mod.name] = ideo_mod(viewpoints)

def populate_global_vars(viewpoints):
  populate_ideologies(viewpoints)
  populate_ideo_mods(viewpoints)

def axis_metric(m1, m2):
  # return abs(m1 - m2)
  return (m1 - m2) ** 2

def get_max_axis_dist(n):
  return axis_metric(IDE_MIN_VALUE, IDE_MAX_VALUE) * n

def get_axis_dist(axis1, axis2):
  distance = 0
  for axis in axis2.keys():
    distance += axis_metric(axis1[axis], axis2[axis])
  return distance

def calc_axis_deviations(axis1, axis2):
  value_deviations = {}
  for axis in axis1.keys():
    if axis not in axis2.keys():
      value_deviations[axis] = IDE_NONE
      continue
    value_deviations[axis] = axis1[axis] - axis2[axis]
  return value_deviations

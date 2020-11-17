import math
import random

import global_vars as gv

from heapq import heappush, heappop

from .helpers import get_all_subclasses, populate_ideologies, populate_ideo_mods, get_axis_dist, get_max_axis_dist, calc_axis_deviations
from .roguelike.modifiable_string import ModifiableString

from .defines import IDE_NONE, IDE_MOD_MAX_DIST_MULT, IDE_MIN_VALUE, IDE_MAX_VALUE

class Worldview:
  def __init__(self, pos_viewpoints, saveObject={}):
    self.ideology_name = ModifiableString("")

    self.ideology_foreground = "#000000"
    self.ideology_background = "#000000"

    self.current_mods = []

    self.viewpoints = {}

    for viewpoint in pos_viewpoints:
      if("viewpoints" in saveObject.keys() and viewpoint.name in saveObject["viewpoints"].keys()):
        view_type = str_to_class(saveObject["viewpoints"][viewpoint.name]["type"])
        view = view_type.load_save_state(saveObject["viewpoints"][viewpoint.name])

      else:
        view = viewpoint()

        view.value = random.randrange(IDE_MIN_VALUE, IDE_MAX_VALUE + 1)
        view.stubborness = random.uniform(0.0, 1.0)
        view.persuasiveness = random.uniform(0.0, 1.0)

      self.viewpoints[view.name] = view

    self.update_ideology_name()

  def generate_political_axis(self):
    axis = {}
    for viewpoint_name in self.viewpoints:
      axis[viewpoint_name] = self.viewpoints[viewpoint_name].value
    return axis

  def update_ideology_name(self):
    if len(gv.IDEOLOGIES) == 0:
      populate_ideologies(self.viewpoints.values())

    my_axis = self.generate_political_axis()

    pos_ideologies = []

    for ideology in gv.IDEOLOGIES.values():
      max_dist = get_max_axis_dist(len(ideology.values))
      distance = get_axis_dist(my_axis, ideology.values)

      heappush(pos_ideologies, (distance / max_dist, ideology))

    closest_ideo = heappop(pos_ideologies)[1]
    self.ideology_name.def_value = closest_ideo.name

    for mod in self.current_mods:
      self.ideology_name.clearModifierSource(mod.name)

    if len(gv.IDE_MODS) == 0:
      populate_ideo_mods(self.viewpoints.values())

    value_deviations = calc_axis_deviations(my_axis, closest_ideo.values)

    pos_mods = self.get_modifiers_heap(value_deviations)

    self.current_mods = []

    while len(pos_mods) > 0:
      new_mod = heappop(pos_mods)[1]
      self.current_mods.append(new_mod)

      value_deviations = calc_axis_deviations(value_deviations, new_mod.values)

      pos_mods = self.get_modifiers_heap(value_deviations)

    source_mod = {}
    for mod in self.current_mods:
      if mod.name not in source_mod.keys():
        source_mod[mod.name] = []
      source_mod[mod.name].append(mod.text_mod)

    self.ideology_name.addModifiersSource(source_mod)

  def get_modifiers_heap(self, value_deviations):
    pos_mods = []

    for ideo_mod in gv.IDE_MODS.values():
      distance = get_axis_dist(value_deviations, ideo_mod.values)
      max_dist = get_max_axis_dist(len(ideo_mod.values))
      if distance > max_dist * IDE_MOD_MAX_DIST_MULT:
        continue

      # print(ideo_mod.name, ":", distance, "/", max_dist, "(" + str(get_max_axis_dist(len(ideo_mod.values))) + ")")

      heappush(pos_mods, (distance / max_dist, ideo_mod))
    return pos_mods

  def get_sentence(self, pos_viewpoints, viewpoints_points, viewpoints_offense_points, citizen_vocality, targets_text):
    sentence = ""
    sentence_beggining = True
    first_word = (not print_say_target or targets_text == "") # Since if we're printing the target-defining text, we don't need to capitalize the first word. In fact, the next word we speak won't be the first word...
    points_list_len = len(pos_viewpoints)

    random.shuffle(pos_viewpoints)  # So we randomly say our opinions on different matters, not strictly in row each time.

    """
    A weird but neccessary hack. We do not randomize offenses, since they are directed at ideologies we do not like.
    So if it so happens that we don't have something to say about a certain viewpoint after shuffle of words per viewpoint,
    we just don't.

    START HACK.
    """

    n = points_list_len - 1
    while(n >= 0):
      point = pos_viewpoints[n]

      if(viewpoints_points[n] == 0 and viewpoints_offense_points[pos_viewpoints[n]] == 0):
        pos_viewpoints.remove(pos_viewpoints[n])
        viewpoints_points.pop(n)
        points_list_len -= 1

      n -= 1

    """
    END HACK.
    """

    for n in range(points_list_len):
      if(not sentence_beggining):
          sentence += " "
      else:
          sentence_beggining = False

      point = self.viewpoints[pos_viewpoints[n]]
      points_total = viewpoints_points[n] + viewpoints_offense_points[pos_viewpoints[n]]

      word_pos = 1
      while(viewpoints_points[n] != 0 or viewpoints_offense_points[pos_viewpoints[n]] != 0):
        word_uppercase = WORD_UPPERCASE_NONE

        if(prob(abs(point.value * point.stubborness * citizen_vocality))):  # We tend to shout when speaking about things we like.
          word_uppercase = WORD_UPPERCASE_UPPER
        elif(first_word):
          word_uppercase = WORD_UPPERCASE_CAPITALIZE

        word_to_say = ""

        if(viewpoints_offense_points[pos_viewpoints[n]] != 0 and (viewpoints_points[n] == 0 or prob(50))):
          word_to_say = point.get_offense(uppercase=word_uppercase)
          viewpoints_offense_points[pos_viewpoints[n]] -= 1
        elif(viewpoints_points[n] != 0):
          word_to_say = point.get_word(uppercase=word_uppercase)
          viewpoints_points[n] -= 1

        if(word_pos == points_total):
          if(n == points_list_len - 1):
            delimetre = random.choice(DELIMETERS_SENTENCE_END)
            sentence += word_to_say + delimetre
            first_word = True
          else:
            delimetre = random.choice(DELIMETERS)
            sentence += word_to_say + delimetre
            if(delimetre in DELIMETERS_SENTENCE_END):
              first_word = True
            else:
              first_word = False

        else:
          sentence += word_to_say + " "
          first_word = False

        word_pos += 1

    return sentence

  def get_save_state(self):
    saveObject = {}
    saveObject["type"] = type(self).__name__

    saveObject["viewpoints"] = {}
    for viewpoint_name in self.viewpoints.keys():
      saveObject["viewpoints"][viewpoint_name] = self.viewpoints[viewpoint_name].get_save_state()

    return saveObject

  def load_save_state(saveObject):
    me = str_to_class(saveObject["type"])(saveObject)
    return me

"""
!!!DISCLAIMER!!!
ALL INFORMATION CONTAINED IN THIS FILE HAS NOTHING TO DO WITH REAL LIFE.
ALL CHARACTERS DESCRIBED HERE ARE FICTIONARY.
ANY AND ALL SIMILARITIES ARE COMPLETELY COINCIDENTAL.
"""

import random

from config_loader import CONFIG_VALUES as CFG

from locale_game import LOCALE

from defines import *

LOCALE_LANGUAGE = CFG["LOCALE_LANGUAGE"]


class Viewpoint:
    name = "Political View"

    pos_name = ""  # Positive, as in positive values.
    pos_color = "white"
    pos_words = []
    pos_offended_by = []

    neg_name = ""  # Negative, as in negative values.
    neg_color = "black"
    neg_words = []
    neg_offended_by = []

    def __init__(self):
        self.value = 0  # From 100(Left part of name) to -100(Right)
        self.stubborness = 1.0  # A rate at which we can change this view of the person.
        self.persuasiveness = 1.0  # A rate at which we can convince others of this view.

    def get_name(self, value):
        if(value == 0):
            return random.choice([pos_name, neg_name])
        if(value > 0):
            return pos_name
        else:
            return neg_name

    def get_word(self, uppercase=WORD_UPPERCASE_NONE):
        word = ""

        if(self.value == 0):
            to_choose = []
            to_choose.extend(self.pos_words)
            to_choose.extend(self.neg_words)
            word = random.choice(to_choose)
        elif(self.value > 0):
            word = random.choice(self.pos_words)
        else:
            word = random.choice(self.neg_words)

        if(uppercase == WORD_UPPERCASE_NONE):
            return word
        elif(uppercase == WORD_UPPERCASE_CAPITALIZE):
            return word.capitalize()
        elif(uppercase == WORD_UPPERCASE_UPPER):
            return word.upper()

    def get_offense(self, uppercase=WORD_UPPERCASE_NONE):
        word = ""

        if(self.value == 0):
            to_choose = []
            to_choose.extend(self.pos_offended_by)
            to_choose.extend(self.neg_offended_by)
            word = random.choice(to_choose)
        elif(self.value < 0):
            word = random.choice(self.pos_offended_by)
        else:
            word = random.choice(self.neg_offended_by)

        if(uppercase == WORD_UPPERCASE_NONE):
            return word
        elif(uppercase == WORD_UPPERCASE_CAPITALIZE):
            return word.capitalize()
        elif(uppercase == WORD_UPPERCASE_UPPER):
            return word.upper()

    def get_color(self, value):
        if(value == 0):
            return random.choice([pos_color, neg_color])
        if(value > 0):
            return pos_color
        else:
            return neg_color

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["value"] = self.value
        saveObject["stubborness"] = self.stubborness
        saveObject["persuasiveness"] = self.persuasiveness

        return saveObject

    def load_save_state(saveObject):
        from politics import str_to_class

        me = str_to_class(saveObject["type"])()

        me.value = saveObject["value"]
        me.stubborness = saveObject["stubborness"]
        me.persuasiveness = saveObject["persuasiveness"]

        return me


class Lib_Aut(Viewpoint):
    name = "Liberty-Authority"

    pos_name = "Liberty"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Liberty"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Liberty_Offensive"]

    neg_name = "Authority"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Authority"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Authority_Offensive"]


class Paci_Mili(Viewpoint):
    name = "Pacifism-Militarism"

    pos_name = "Pacifism"
    pos_color = "Green"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Pacifism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Pacifism_Offensive"]

    neg_name = "Militarism"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Militarism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Militarism_Offensive"]


class Mat_Spi(Viewpoint):
    name = "Materialism-Spiritualism"

    pos_name = "Materialism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Materialism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Materialism_Offensive"]

    neg_name = "Spiritualism"
    neg_color = "Purple"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Spiritualism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Spiritualism_Offensive"]


class Ind_Col(Viewpoint):
    name = "Individualism-Collectivism"

    pos_name = "Individualism"
    pos_color = "Purple"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Individualism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Individualism_Offensive"]

    neg_name = "Collectivism"
    neg_color = "Gray"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Collectivism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Collectivism_Offensive"]


class Ref_Rev(Viewpoint):
    name = "Reformism-Revolutionism"

    pos_name = "Reformism"
    pos_color = "Gray"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Reformism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Reformism_Offensive"]

    neg_name = "Revolutionism"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Revolutionism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Revolutionism_Offensive"]


class Ind_Pri(Viewpoint):
    name = "Industrialism-Primitivism"

    pos_name = "Industrialism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Industrialism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Industrialism_Offensive"]

    neg_name = "Primitivism"
    neg_color = "Green"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Primitivism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Primitivism_Offensive"]

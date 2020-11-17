"""
!!!DISCLAIMER!!!
ALL INFORMATION CONTAINED IN THIS FILE HAS NOTHING TO DO WITH REAL LIFE.
ALL CHARACTERS DESCRIBED HERE ARE FICTIONARY.
ANY AND ALL SIMILARITIES ARE COMPLETELY COINCIDENTAL.
"""

# TO-DO: rename pos-neg to left-right.

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

class Civility(Viewpoint):
    """
    Civility is a political axis that determines the actions that are allowed to an agent in opposition to the other.
    Liberty is basically "an agent is allowed anything"
    Authority is thus "the other controls what an agent is allowed"
    """
    name = "Civility"

    pos_name = "Liberty"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Liberty"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Liberty_Offensive"]

    neg_name = "Authority"
    neg_color = "Blue"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Authority"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Authority_Offensive"]

class Mastery(Viewpoint):
    """
    Mastery is a political axis that determines the ideologies view on enforcing the ideology onto others.
    Insularity is basically "do not enforce the ideology onto others"
    Dominance is "enforce the ideology onto others"
    """
    name = "Mastery"

    pos_name = "Insularity"
    pos_color = "Grey"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Insularity"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Insularity_Offensive"]

    neg_name = "Dominance"
    neg_color = "Green"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Dominance"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Dominance_Offensive"]


class Impactfulness(Viewpoint):
    """
    Impactfulness is a political axis that determines how the world should change to fit in with the ideology.
    Revolutionism is about changing the status-quo as quickly as possible, direct action, and etc.
    Reformism is a movement for saving the status-quo, and the less invasive forms and methods of change.
    """
    name = "Impactfulness"

    pos_name = "Revolutionism"
    pos_color = "Red"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Revolutionism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Revolutionism_Offensive"]

    neg_name = "Reformism"
    neg_color = "Gray"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Reformism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Reformism_Offensive"]

class Proprietary(Viewpoint):
    """
    Proprietary is an economic axis that determines who and how the stuff is owned.
    Altruity is basically "property does not exist".
    Avarice is basically "all the property to those who matter", where "matter" is defined by other axis.
    """
    name = "Proprietary"

    pos_name = "Altruity"
    pos_color = "Red"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Altruity"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Altruity_Offensive"]

    neg_name = "Avarice"
    neg_color = "Yellow"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Avarice"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Avarice_Offensive"]

class Narrative(Viewpoint):
    """
    Narrative is a political axis that determines the belief of how an ideology is formed and reached at.
    Constructivism is the belief that this ideology is a product of individual/social/governmental construction.
    Essentialism is the belief that this ideology will be naturally arrived at by any forces at play.
    """
    name = "Narrative"

    pos_name = "Constructivism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Constructivism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Constructivism_Offensive"]

    neg_name = "Essentialism"
    neg_color = "Green"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Essentialism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Essentialism_Offensive"]


class Atomarity(Viewpoint):
    """
    Atomarity is a political axis that determines at what level should anything political be viewed from.
    Collectivism is the focus on the system as a whole.
    Individualism is using the smallest possible atom of the thing in question.
    """
    name = "Atomarity"

    pos_name = "Collectivism"
    pos_color = "Gray"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Collectivism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Collectivism_Offensive"]

    neg_name = "Individualism"
    neg_color = "Purple"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Individualism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Individualism_Offensive"]

class Wishfulness(Viewpoint):
    """
    Wishfulness is an axis that determines where does this ideology place it's atom in regards to "the big picture".
    Pessimism is saying the atom doesn't matter in "the big picture".
    Optimism is saying the atom is the only thing that matters in "the big picture".
    """
    name = "Wishfulness"

    pos_name = "Pessimism"
    pos_color = "Aquamarine"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Pessimism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Pessimism_Offensive"]

    neg_name = "Optimism"
    neg_color = "Orange"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Optimism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Optimism_Offensive"]

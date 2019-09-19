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
    """
    Liberty is the movement for lesser intrusion into each individual's life in any shape or form. Be it government, corporative, etc...
    Authority is thus, the complete opposite.
    """
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
    """
    Pacifism is not disregard for war, but for violence and violent methods of ANYTHING in general.
    Militarism is thus, the opposite.
    """
    name = "Pacifism-Militarism"

    pos_name = "Pacifism"
    pos_color = "Green"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Pacifism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Pacifism_Offensive"]

    neg_name = "Militarism"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Militarism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Militarism_Offensive"]


class Int_Ext(Viewpoint):
    """
    Intensivism is the practice of thoughtfully distributing limited resources.
    Extensivism is the practice of gathering MORE resources each time they are not abundant.
    """
    name = "Intensivism-Extensivism"

    pos_name = "Intensivism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Intensivism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Intensivism_Offensive"]

    neg_name = "Extensivism"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Extensivism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Extensivism_Offensive"]

"""
class Mat_Spi(Viewpoint):
    '''
    Materialism is the denial of non-material essences, objects, subjects, phenomena.
    Spiritualism is the acceptance, and even embracement of the non-material.
    '''
    name = "Materialism-Spiritualism"

    pos_name = "Materialism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Materialism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Materialism_Offensive"]

    neg_name = "Spiritualism"
    neg_color = "Purple"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Spiritualism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Spiritualism_Offensive"]
"""

class Ind_Col(Viewpoint):
    """
    Individualism is the focus on needs of an individual, as opposed to...
    Collectivism is the focus on needs of THE group, THE "majority", THE "all".
    """
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
    """
    Reformism is a movement for saving the status-quo, and the less invasive forms and methods of change.
    Revolutionism is an opposite to Reformism.
    """
    name = "Reformism-Revolutionism"

    pos_name = "Reformism"
    pos_color = "Gray"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Reformism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Reformism_Offensive"]

    neg_name = "Revolutionism"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Revolutionism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Revolutionism_Offensive"]


class Con_Ess(Viewpoint):
    """
    Constructivism is the movement that say solutions to problems lie in man-made anything.
    Essentialism is the movement that suggests that such solutions are already out there, and we only need to discover them.
    """
    name = "Constructivism-Essentialism"

    pos_name = "Constructivism"
    pos_color = "Yellow"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Constructivism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Constructivism_Offensive"]

    neg_name = "Essentialism"
    neg_color = "Green"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Essentialism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Essentialism_Offensive"]


class Den_Acc(Viewpoint):
    """
    Denial is in a sense, a form of nihilism, denial of anything: reason, logic, truth.
    Acceptance is the claim that all of the above actually are true, or do exist.
    """
    name = "Denial-Acceptance"

    pos_name = "Denial"
    pos_color = "Blue"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Denial"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Denial_Offensive"]

    neg_name = "Acceptance"
    neg_color = "Red"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Acceptance"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Acceptance_Offensive"]

"""
class Hed_Asc(Viewpoint):
    '''
    Hedonism is embracing any lustful activity an individual, or a collective can perform.
    Asceticism is a form of restraint from those activities.
    '''
    name = "Hedonism-Asceticism"

    pos_name = "Hedonism"
    pos_color = "Purple"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Hedonism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Hedonism_Offensive"]

    neg_name = "Asceticism"
    neg_color = "Grey"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Asceticism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Asceticism_Offensive"]
"""

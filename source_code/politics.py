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

import os
import time
import random
import re
import math

import config_loader
from config_loader import CONFIG_VALUES as CFG

from color_printer import ColorPrinter
from locale_game import LOCALE
from ideologies_game import IDEOLOGIES_CLASSIFICATION

"""
Setting up CONFIG.
"""
CONFIG_REQUEST = {
    "DEBUG": {"cfg_type": "bool", "def_value": False},  # config_loader only outputs messages if this is True.

    "IS_SERVER": {"cfg_type": "bool", "def_value": False},
    "SECRET_KEY": {"cfg_type": "key"},  # This is not in the config.cfg, as it is always generated completely at random.
    "PORT": {"cfg_type": "int", "def_value": 8080, "min_val": 0, "max_val": 65535},
    "UPDATE_CACHE": {"cfg_type": "bool", "def_value": False},

    "LOCALE_LANGUAGE": {"cfg_type": "str", "def_value": "en", "min_val": 0, "max_val": 2, "possible_values": ["en", "ru", "la"]},

    "MAX_WORDS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},
    "MAX_TARGETS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},

    "DEFAULT_RELATIONSHIP_SHIFT_VALUE": {"cfg_type": "float", "def_value": 2.0, "min_val": 0.0, "max_val": 100.0},
    "INITIAL_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": 1.0, "min_val": -100.0, "max_val": 100.0, "prohibited_values": [0.0]},

    "DEFAULT_MIN_POSSIBLE_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": -10.0, "min_val": -100.0, "max_val": 100.0},
    "DEFAULT_MAX_POSSIBLE_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": 10.0, "min_val": -100.0, "max_val": 100.0},

    "RELATIONSHIP_MIN_MODIFIER_ON_OFFENSE": {"cfg_type": "float", "def_value": 0.1, "min_val": -100.0, "max_val": 100.0},
    "RELATIONSHIP_MAX_MODIFIER_ON_CRIT_PERSUASION": {"cfg_type": "float", "def_value": 1.0, "min_val": -100.0, "max_val": 100.0},

    "DISLIKE_WORDS_MAXIMUM": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 1.0},

    "DISLIKE_OFFENSES_MINIMUM": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 1.0},
    "OFFENSE_RELATIONSHIP_MULTIPLIER": {"cfg_type": "float", "def_value": 3.0, "min_val": -100.0, "max_val": 100.0},

    "DEFAULT_PERSUASION_MULTIPLIER": {"cfg_type": "float", "def_value": 2.0, "min_val": -100.0, "max_val": 100.0},
    "CRIT_PERSUASION_MULTIPLIER": {"cfg_type": "float", "def_value": 10.0, "min_val": -100.0, "max_val": 100.0},
    "CRIT_PERSUASION_DISLIKE_MULTIPLIER": {"cfg_type": "float", "def_value": 0.0, "min_val": -100.0, "max_val": 100.0},

    "print_viewpoint_shifts": {"cfg_type": "bool", "def_value": True},
    "print_ideology_changes": {"cfg_type": "bool", "def_value": True},
    "stop_on_ideology_change": {"cfg_type": "bool", "def_value": True},

    "print_relationship_shifts": {"cfg_type": "bool", "def_value": True},
    "print_relationship_changes": {"cfg_type": "bool", "def_value": True},
    "stop_on_relationship_change": {"cfg_type": "bool", "def_value": True},

    "print_say_target": {"cfg_type": "bool", "def_value": True},

    "between_messages_delay_min": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 10.0},
    "between_messages_delay_max": {"cfg_type": "float", "def_value": 2.0, "min_val": 0.0, "max_val": 10.0}
}

config_loader.main(CONFIG_REQUEST)

"""
Global, constant variables.
"""
# See config_loader.py for more detail.

WORD_UPPERCASE_NONE = 0
WORD_UPPERCASE_CAPITALIZE = 1
WORD_UPPERCASE_UPPER = 2

WORD_UPPERCASE_POSSIBILITIES = [WORD_UPPERCASE_NONE, WORD_UPPERCASE_CAPITALIZE, WORD_UPPERCASE_UPPER]

DELIMETERS = [".", "!", "?", ",", "", ":"]
DELIMETERS_SENTENCE_END = [".", "!", "?"]

UP_ARROW_SYMBOL = "\u2191"
DOWN_ARROW_SYMBOL = "\u2193"

NAME_LETTERS = ["A", "a"]  # Is used when we have a name collision.

"""
Locale. And all related to it.
"""
# See imports.

LOCALE_LANGUAGE = CFG["LOCALE_LANGUAGE"]

"""
Global, but not neccesarily constant variables.
"""
print_viewpoint_shifts = CFG["print_viewpoint_shifts"]  # Whether we print messages such as "LA^3.0".
print_ideology_changes = CFG["print_ideology_changes"]  # Whether we print message such as "A changed their ideology from: B to: C".
stop_on_ideology_change = CFG["stop_on_ideology_change"]  # Whether we stop the simulation on the ideology change message.

print_relationship_shifts = CFG["print_relationship_shifts"]  # Whether we print messages such as "changed their relation to: |^10.0|".
print_relationship_changes = CFG["print_relationship_changes"]  # Whether we print messages such as "A now hates B".
stop_on_relationship_change = CFG["stop_on_relationship_change"]  # Whether we stop the simulation on the relationhip change message.

print_say_target = CFG["print_say_target"]  # Whether we print whom the message is adressed(If TRUE, messages will be of form: "A, B, C: I WANT TO SAY D").

# A delay between messages, if any.
between_messages_delay_min = CFG["between_messages_delay_min"]
between_messages_delay_max = CFG["between_messages_delay_max"]

viewpoints_by_word = {}
offensive_to_viewpoint = {}

locale_to_original = {}
original_to_locale = {}

taken_clean_citizen_names = []  # Clean currently means lowercase.

RELATIONSHIP_THRESHOLDS = [
    {"Name": LOCALE[LOCALE_LANGUAGE]["Reverence"], "Min": 90, "Max": 100, "Color": 'g'},
    {"Name": LOCALE[LOCALE_LANGUAGE]["Respect"], "Min": 50, "Max": 90, "Color": 'g'},
    {"Name": LOCALE[LOCALE_LANGUAGE]["Sympathy"], "Min": 25, "Max": 50, "Color": 'w'},
    {"Name": LOCALE[LOCALE_LANGUAGE]["Distaste"], "Min": -50, "Max": -25, "Color": 'w'},
    {"Name": LOCALE[LOCALE_LANGUAGE]["Hate"], "Min": -90, "Max": -50, "Color": 'r'},
    {"Name": LOCALE[LOCALE_LANGUAGE]["Feud"], "Min": -100, "Max": -90, "Color": 'r'}
]

"""
Lambda functions and functions.
"""
sign = lambda x: math.copysign(1, x)  # Gets sign of x.

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))

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
    return original_to_locale[random.choice(closest_approximations[min(closest_approximations.keys(), key=float)])]

def init_viewpoints_by_words_list():
    pos_viewpoints = get_all_subclasses(Viewpoint)
    for viewpoint in pos_viewpoints:
        for word in viewpoint.pos_words:
            viewpoints_by_word[word] = {"Viewpoint": viewpoint.name, "Value": 1}
        for word in viewpoint.neg_words:
            viewpoints_by_word[word] = {"Viewpoint": viewpoint.name, "Value": -1}

        for word in viewpoint.pos_offended_by:
            offensive_to_viewpoint[word] = {"Viewpoint": viewpoint.name, "Value": 1}
        for word in viewpoint.neg_offended_by:
            offensive_to_viewpoint[word] = {"Viewpoint": viewpoint.name, "Value": -1}

def init_locale_relate_original():
    for original_item, locale_item in LOCALE[LOCALE_LANGUAGE].items():
        if(type(locale_item) is list):
            continue
            """

            If you want to reference the pairs of word and their translations in lists such as EN_PRIMITIVISM_WORDS you'd need to rework all of this.

            for locale_item_in_list in locale_item:
                locale_to_original
            """
        locale_to_original[locale_item] = original_item
        original_to_locale[original_item] = locale_item

def init_reference_lists():
    init_viewpoints_by_words_list()
    init_locale_relate_original()


def prob(probability):
    if(random.randint(1, 100) <= probability):
        return True
    return False


def pick_weighted(seq):
    choices = []
    for key in seq:
        amount = seq[key]
        for choice in range(amount):
            choices.append(key)
    return random.choice(choices)


def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def to_chat(text):
    if(CFG["IS_SERVER"]):
        socketio.emit('npc_message', {"data": text})
    else:
        print(text)


class Citizen:
    def __init__(self, name, views_preset=dict()):
        while(name.lower() in taken_clean_citizen_names):
            name = name + random.choice(NAME_LETTERS)

        taken_clean_citizen_names.append(name.lower())

        self.age = 1
        self.name = name

        if("Vocal" in views_preset):
            self.vocal = views_preset["Vocal"]
        else:
            self.vocal = random.uniform(0.0, 1.0)  # How vocal we are about our opinions. Where 0 is not vocal at all, and 1 is very vocal.

        if("Tolerancy" in views_preset):
            self.tolerancy = views_preset["Tolerancy"]
        else:
            self.tolerancy = random.uniform(0.0, 1.0)  # How hard we hate people with other ideologies, and how often we try to offend them.

        self.political_view = View(views_preset)

        self.ideology_name = get_closest_ideology(self.political_view.generate_political_axis())

        self.favour_words = {}
        self.dislike_words = {}
        self.generate_words_relation()
        self.favour_intonations = {}
        self.dislike_intonations = {}
        self.generate_intonations_relation()
        self.favour_word_uppercase = {}
        self.dislike_word_uppercase = {}
        self.generate_uppercase_relation()

        self.relationships = {}
        for citizen in citizens:
            self.relationships[citizen.name] = Relationship()
            self.adjust_relationship_value(citizen, CFG["INITIAL_RELATIONSHIP_VALUE"])
            citizen.relationships[self.name] = Relationship()
            citizen.adjust_relationship_value(self, CFG["INITIAL_RELATIONSHIP_VALUE"])

    def generate_words_relation(self):
        for word in viewpoints_by_word:
            self.favour_words[word] = random.uniform(0.0, 1.0)  # How much we like this word(it may persuade us more). Where 0 is we don't like it at all, 1 is we like the word very much.
            self.dislike_words[word] = random.uniform(0.0, CFG["DISLIKE_WORDS_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

        for offense in offensive_to_viewpoint.keys():
            self.favour_words[offense] = 0.0
            self.dislike_words[offense] = random.uniform(CFG["DISLIKE_OFFENSES_MINIMUM"], 1.0)

        self.favour_words[LOCALE[LOCALE_LANGUAGE]["All"].lower()] = random.uniform(0.0, 1.0)
        self.dislike_words[LOCALE[LOCALE_LANGUAGE]["All"].lower()] = 0.0

        clean_name = self.name.lower()

        self.favour_words[clean_name] = random.uniform(0.0, 1.0)
        self.dislike_words[clean_name] = 0.0
        for citizen in citizens:
            citizen.favour_words[clean_name] = random.uniform(0.0, 1.0)
            citizen.dislike_words[clean_name] = 0.0

            clean_citizen_name = citizen.name.lower()

            self.favour_words[clean_citizen_name] = random.uniform(0.0, 1.0)
            self.dislike_words[clean_citizen_name] = 0.0

    def generate_intonations_relation(self):
        for intonation in DELIMETERS_SENTENCE_END:
            self.favour_intonations[intonation] = random.uniform(0.0, 1.0)  # How much we like this intonation. Where 0 is we don't like it at all, 1 is we like the word very much.
            self.dislike_intonations[intonation] = random.uniform(0.0, 1.0)  # It may be convincing, but we may dislike it on emotional level.

    def generate_uppercase_relation(self):
        for word_uppercase in WORD_UPPERCASE_POSSIBILITIES:
            self.favour_word_uppercase[word_uppercase] = random.uniform(0.0, 1.0)  # How much we like when the word is shouted, or said with uppercase. Where 0 is we don't like it at all, 1 is we like the word very much.
            self.dislike_word_uppercase[word_uppercase] = random.uniform(0.0, 1.0)  # It may be convincing, but we may dislike it on emotional level.

    def say(self):
        targets_amount = round(CFG["MAX_TARGETS"] * random.uniform(0.0, self.vocal))
        if(targets_amount == 0):
            return

        words_amount = round(CFG["MAX_WORDS"] * random.uniform(0.0, self.vocal))
        if(words_amount == 0):
            return

        targets_text = ""
        targets = []
        if(targets_amount == CFG["MAX_TARGETS"]):
            targets_text = LOCALE[LOCALE_LANGUAGE]["All"] + ": "
        else:
            first_target = True

            for t in range(targets_amount):
                new_target = random.choice(citizens)
                if(targets_text.find(new_target.name) >= 0):  # We are already shouting to them.
                    continue
                if(new_target == self):  # Don't talk to yourself... TODO: Add instanity.
                    continue
                if(not first_target):
                    targets_text += ", "
                first_target = False
                new_target_name = new_target.name
                if(prob(self.vocal * 100)):
                    new_target_name.upper()

                targets_text += new_target_name
                targets.append(new_target)
            if(not first_target):
                targets_text += ": "

        pos_viewpoints = []
        viewpoints_points = []
        viewpoints_offense_points = {}
        for viewpoint in self.political_view.viewpoints:
            if(words_amount <= 1):
                break
            cur_point_am = abs(round(random.randrange(1, words_amount) * random.uniform(0.0, self.political_view.viewpoints[viewpoint].value / 100)))
            cur_offense_points_am = 0
            if(cur_point_am > 0):
                try:
                    for target in targets:
                        if(self.offend_target_prob(target, viewpoint)):
                            cur_offense_points_am += 1
                            cur_point_am -= 1
                            if(cur_point_am == 0):
                                raise StopIteration
                    raise StopIteration
                except StopIteration:
                    if(cur_point_am != 0 or cur_offense_points_am != 0):
                        pos_viewpoints.append(viewpoint)
                        viewpoints_points.append(cur_point_am)
                        viewpoints_offense_points[viewpoint] = cur_offense_points_am
                        words_amount -= cur_point_am
                        words_amount -= cur_offense_points_am

        sentence = self.political_view.get_sentence(pos_viewpoints, viewpoints_points, viewpoints_offense_points, self.vocal)
        verb = self.get_verb(sentence)

        if(len(sentence) == 0):
            sentence = "..."

        print_sentence = sentence
        sentence = targets_text + sentence
        if(print_say_target):
            print_sentence = targets_text + print_sentence

        to_chat(ColorPrinter.fmt(self.name, fg='c', style="b") +
                ColorPrinter.fmt("(", fg='c') +
                ColorPrinter.fmt(self.ideology_name, fg='w') +
                ColorPrinter.fmt(") ", fg='c') +
                ColorPrinter.fmt(verb + ", ", fg='c', style="i") +
                ColorPrinter.fmt("\"", fg='c') +
                print_sentence +
                ColorPrinter.fmt("\"", fg='c'))

        to_hear = citizens.copy()
        to_hear.remove(self)

        for citizen in to_hear:
            citizen.hear(self, verb, sentence)

    def hear(self, speaker, verb, sentence):
        intonation_delimeter = sentence[len(sentence) - 1]

        delimeters_to_remove = "".join(DELIMETERS)
        sentence_stripped = re.sub("[" + delimeters_to_remove + "]", "", sentence)
        sentence_stripped = sentence_stripped.strip()  # Remove trailing spaces.
        words = []
        if(len(sentence_stripped) > 0):
            words = sentence_stripped.split(" ")

        can_hear = False

        if(self.relationships[speaker.name].title in ["Reverence", "Feud"]):  # We listen to our friends, and to enemies.
            if(self.listen_to_speaker_check(speaker, word, verb, sentence)):
                can_hear = True

        if(not can_hear):
            to_check = len(words) - 1
            while(to_check >= 0):
                word = words[to_check]
                clean_word = word.lower()

                clean_all_word = LOCALE[LOCALE_LANGUAGE]["All"].lower()

                """
                Offensive words should instantly grab our attention.
                """
                if(clean_word in offensive_to_viewpoint.keys()):
                    point = offensive_to_viewpoint[clean_word]["Viewpoint"]
                    point_value = self.political_view.viewpoints[point].value

                    # If they said something offensive, check if we hear them!
                    if(sign(point_value) == sign(offensive_to_viewpoint[clean_word]["Value"]) and self.listen_to_speaker_check(speaker, word, verb, sentence)):
                        can_hear = True
                        break

                if(clean_word == self.name.lower() or clean_word == clean_all_word):
                    if(self.listen_to_speaker_check(speaker, word, verb, sentence)):
                        can_hear = True
                        break

                to_check -= 1

        if(not can_hear or len(words) == 0):
            return

        shifted_viewpoints = {}
        relationship_shift = 0
        for word in words:
            retVal = self.react_word(speaker, verb, intonation_delimeter, word)
            if(retVal["Viewpoint"] != ""):
                if(retVal["Viewpoint"] in shifted_viewpoints):
                    shifted_viewpoints[retVal["Viewpoint"]] += retVal["Viewpoint_Shift_Value"]
                else:
                    shifted_viewpoints[retVal["Viewpoint"]] = retVal["Viewpoint_Shift_Value"]
            relationship_shift += retVal["Relationship_Shift_Value"]

        shift_occured = False
        convinced_string = ColorPrinter.fmt("|", fg='b')

        old_ideology_name = self.ideology_name

        for viewpoint_shift in shifted_viewpoints:
            retVal = self.adjust_viewpoint_value(viewpoint_shift, shifted_viewpoints[viewpoint_shift])
            if(retVal == 0.0):
                continue

            shift_occured = True

            if(not print_viewpoint_shifts):
                continue

            viewpoint_words = viewpoint_shift.split("-")
            letters = ""
            for viewpoint_word in viewpoint_words:
                letters += viewpoint_word[0]

            shift_sign = sign(retVal)

            arrow_indicator = ''
            color_indicator = ''

            if(shift_sign > 0.0):
                arrow_indicator = UP_ARROW_SYMBOL
                color_indicator = 'g'
            else:
                arrow_indicator = DOWN_ARROW_SYMBOL
                color_indicator = 'r'

            convinced_string += ColorPrinter.fmt(letters + arrow_indicator + str(round(retVal, 1)), fg=color_indicator)
            convinced_string += ColorPrinter.fmt("|", fg='b')

        if(shift_occured):
            self.ideology_name = get_closest_ideology(self.political_view.generate_political_axis())

            if(print_viewpoint_shifts):
                to_chat(ColorPrinter.fmt(speaker.name, fg='b', style='b') +
                        ColorPrinter.fmt(" " + LOCALE[LOCALE_LANGUAGE]["Convinced"] + " ", fg='b', style='i') +
                        ColorPrinter.fmt(self.name, fg='b', style='b') +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["Announcement_end"], fg='b', style='i') +
                        " " + convinced_string)
            if(print_ideology_changes and old_ideology_name != self.ideology_name):
                to_chat(ColorPrinter.fmt(self.name, fg='b', style='b') +
                        ColorPrinter.fmt(" " + LOCALE[LOCALE_LANGUAGE]["Changed Ideology From"] + ": ", fg='b', style='i') +
                        ColorPrinter.fmt(old_ideology_name, fg='w') +
                        ColorPrinter.fmt(" " + LOCALE[LOCALE_LANGUAGE]["To"] + ": ", fg='b', style='i') +
                        ColorPrinter.fmt(self.ideology_name, fg='w') +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["Announcement_end"], fg='b', style='i'))
                if(stop_on_ideology_change):
                    input_to_stop_chat = input()

        absolute_relationship_shift = self.adjust_relationship_value(speaker, relationship_shift)
        if((absolute_relationship_shift > 0.1 or absolute_relationship_shift < -0.1) and print_relationship_shifts):
            shift_sign = sign(absolute_relationship_shift)

            arrow_indicator = ''
            color_indicator = ''

            if(shift_sign > 0.0):
                arrow_indicator = UP_ARROW_SYMBOL
                color_indicator = 'g'
            else:
                arrow_indicator = DOWN_ARROW_SYMBOL
                color_indicator = 'r'

            relationship_string = ColorPrinter.fmt("|", fg='b')
            relationship_string += ColorPrinter.fmt(arrow_indicator + str(round(absolute_relationship_shift, 1)), fg=color_indicator)
            relationship_string += ColorPrinter.fmt("|", fg='b')

            to_chat(ColorPrinter.fmt(self.name, fg='b', style='b') +
                    ColorPrinter.fmt(" " + LOCALE[LOCALE_LANGUAGE]["Relationship Changed To"], fg='b', style='i') + " " +
                    ColorPrinter.fmt(speaker.name, fg='b', style='b') +
                    ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["Announcement_end"], fg='b', style='i') +
                    " " + relationship_string)

        old_relationship_title = self.relationships[speaker.name].title
        old_relationship_title_color = self.relationships[speaker.name].title_color

        if(self.update_relationship_title(speaker)):  # If it actually did change.
            new_relationship_title = self.relationships[speaker.name].title
            new_relationship_title_color = self.relationships[speaker.name].title_color

            if(print_relationship_changes):
                to_chat(ColorPrinter.fmt(self.name, fg='b', style='b') + " " +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["Relationship Changed To"], fg='b', style='i') + " " +
                        ColorPrinter.fmt(speaker.name, fg='b', style='b') + " " +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["From"], fg='b', style='i') + " " +
                        ColorPrinter.fmt(old_relationship_title, fg=old_relationship_title_color) + " " +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["To"], fg='b', style='i') + " " +
                        ColorPrinter.fmt(new_relationship_title, fg=new_relationship_title_color) +
                        ColorPrinter.fmt(LOCALE[LOCALE_LANGUAGE]["Announcement_end"], fg='b', style='i'))
                if(stop_on_relationship_change):
                    input_to_stop_chat = input()

    def react_word(self, speaker, verb, intonation_delimeter, word):
        """
        How self reacts to speaker's word.
        Returns what viewpoint changed, and by how much in format {"Viewpoint": viewpoint_name, "Value": value_changed}.
        """

        """
        Favour is how critically persuasive the word is.
        Dislike is how much we didn't like it.
        """
        clean_word = word.lower()
        if(clean_word in viewpoints_by_word.keys()):
            base_value = viewpoints_by_word[clean_word]["Value"] * CFG["DEFAULT_PERSUASION_MULTIPLIER"]
            favour = self.favour_words[clean_word] * self.favour_intonations[intonation_delimeter]
        else:  # It's either a filler, or something offensive.
            base_value = 0.0
            favour = 0.0

        relationship_value = CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"]
        dislike = 0

        if(clean_word in offensive_to_viewpoint.keys()):
            point_name = offensive_to_viewpoint[clean_word]["Viewpoint"]
            if(sign(self.political_view.viewpoints[point_name].value) == sign(offensive_to_viewpoint[clean_word]["Value"])):
                dislike = (self.dislike_words[clean_word] + self.dislike_intonations[intonation_delimeter]) * 0.5  # We don't care how offensive the word is if it's not offensive.
                relationship_value *= CFG["OFFENSE_RELATIONSHIP_MULTIPLIER"]  # If it's an offense, it's safe to assume that it'll become negative afterwards.

                self.relationships[speaker.name].permanent_min_val_modifier -= CFG["RELATIONSHIP_MIN_MODIFIER_ON_OFFENSE"]
                self.relationships[speaker.name].permanent_max_val_modifier -= CFG["RELATIONSHIP_MIN_MODIFIER_ON_OFFENSE"]

        if(word.isupper()):
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_UPPER]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_UPPER]) * 0.5  # We do care that we are shouted at.
        elif(word[0].isupper()):  # Checks if capitalized.
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_CAPITALIZE]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_CAPITALIZE]) * 0.5
        else:
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_NONE]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_NONE]) * 0.5

        viewpoint_name = ""
        if(clean_word in viewpoints_by_word.keys()):
            viewpoint_name = viewpoints_by_word[word.lower()]["Viewpoint"]

            base_value *= (1.0 - self.get_stubborness(viewpoint_name)) * speaker.get_persuasiveness(viewpoint_name)

            favour *= (self.relationships[speaker.name].value + 100) / 200  # If we dislike them as a person they have a lower chance to persuade us.

            if(self.crit_persuaded_prob(speaker, viewpoint_name, favour)):
                dislike *= 0.0  # We were very much persuaded. We do not hate this person at all.

                self.relationships[speaker.name].permanent_min_val_modifier += CFG["RELATIONSHIP_MAX_MODIFIER_ON_CRIT_PERSUASION"]
                self.relationships[speaker.name].permanent_max_val_modifier += CFG["RELATIONSHIP_MAX_MODIFIER_ON_CRIT_PERSUASION"]

                base_value *= CFG["CRIT_PERSUASION_DISLIKE_MULTIPLIER"]

        base_value *= (1.0 - dislike)

        relationship_value *= favour - dislike

        # base_value = round(base_value, 1)
        # relationship_value = round(relationship_value, 1)

        return {"Viewpoint": viewpoint_name, "Viewpoint_Shift_Value": base_value, "Relationship_Shift_Value": relationship_value}

    def get_verb(self, sentence):
        sentence_len = len(sentence)

        retVal = "%ERROR OCCURED CONTACT SERVER ADMINISTRATOR OR SOMETHING%"

        if(sentence_len == 0):
            retVal = LOCALE[LOCALE_LANGUAGE]["Mumbles"]
            return retVal
        last_symbol = sentence[sentence_len - 1]
        if(last_symbol == "."):
            retVal = LOCALE[LOCALE_LANGUAGE]["Says"]
        elif(last_symbol == "!"):
            retVal = LOCALE[LOCALE_LANGUAGE]["Exclaims"]
        elif(last_symbol == "?"):
            retVal = LOCALE[LOCALE_LANGUAGE]["Asks"]

        return retVal

    def offend_target_prob(self, target, viewpoint_name):
        # We need a max change of 100, so multiply the thing that goes from 0 to 200 by 0.25 to get 50.
        offend_chance = abs(self.political_view.viewpoints[viewpoint_name].value - target.political_view.viewpoints[viewpoint_name].value) * 0.25
        # The other 50 comes from how much we hate the person.
        offend_chance += (-self.relationships[target.name].value) * 0.5
        return prob(offend_chance * (1.0 - self.tolerancy))

    def crit_persuaded_prob(self, speaker, viewpoint_name, favour):
        return prob((1.0 - self.get_stubborness(viewpoint_name)) * speaker.get_persuasiveness(viewpoint_name) * favour * 100)

    def listen_to_speaker_check(self, speaker, word, verb, sentence):
        intonation_delimeter = sentence[len(sentence) - 1]
        favour = self.favour_intonations[intonation_delimeter]

        if(word.isupper()):
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_UPPER]
        elif(word[0].isupper()):  # Checks if capitalized.
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_CAPITALIZE]
        else:
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_NONE]

        return prob(speaker.vocal * favour * 100)
        

    def get_stubborness(self, viewpoint_name):
        return self.political_view.viewpoints[viewpoint_name].stubborness

    def get_persuasiveness(self, viewpoint_name):
        return self.political_view.viewpoints[viewpoint_name].persuasiveness

    def adjust_viewpoint_value(self, viewpoint_name, value):
        """
        Adjust value of viewpoint_name by argument value.
        Returns by how much we actually changed the value of viewpoint_name.
        """
        if(value < 0.1 and value > -0.1):
            return 0.0

        retVal = round(value, 1)

        self.political_view.viewpoints[viewpoint_name].value += retVal
        if(self.political_view.viewpoints[viewpoint_name].value > 100):
            self.political_view.viewpoints[viewpoint_name].value = 100
            retVal -= self.political_view.viewpoints[viewpoint_name].value - 100
        elif(self.political_view.viewpoints[viewpoint_name].value < -100):
            self.political_view.viewpoints[viewpoint_name].value = -100
            retVal -= self.political_view.viewpoints[viewpoint_name].value + 100
        # self.ideology_name = get_closest_ideology(self.political_view.generate_political_axis())  # Too costly, see hear().
        return retVal

    def update_relationship_title(self, target):
        for relation_type in RELATIONSHIP_THRESHOLDS:
            if(self.relationships[target.name].value >= relation_type["Min"] and
               self.relationships[target.name].value <= relation_type["Max"]):
                if(self.relationships[target.name].title == relation_type["Name"]):
                    return False
                self.relationships[target.name].title = relation_type["Name"]
                self.relationships[target.name].title_color = relation_type["Color"]
                return True

        if(self.relationships[target.name].title == LOCALE[LOCALE_LANGUAGE]["None"]):
            return False

        self.relationships[target.name].title = LOCALE[LOCALE_LANGUAGE]["None"]
        self.relationships[target.name].title_color = 'w'
        return True

    def adjust_relationship_value(self, target, value):
        """
        Adjusts our relationship towards target by value.
        Returns by how much we actually changed the relationship towards them.
        """
        return self.relationships[target.name].adjust_value(self, target, value)

class View:
    def __init__(self, views_preset):
        self.viewpoints = dict()
        pos_viewpoints = get_all_subclasses(Viewpoint)

        for viewpoint in pos_viewpoints:
            view = viewpoint()

            self.viewpoints[view.name] = view
            if(view.name in views_preset):
                view.value = views_preset[view.name]["Value"]
                view.stubborness = views_preset[view.name]["Stubborness"]
                view.persuasiveness = views_preset[view.name]["Persuasiveness"]
            else:
                view.stubborness = random.uniform(0.0, 1.0)
                view.persuasiveness = random.uniform(0.0, 1.0)

    def generate_political_axis(self):
        axis = {}
        for viewpoint_name in self.viewpoints:
            axis[viewpoint_name] = self.viewpoints[viewpoint_name].value
        return axis

    def get_sentence(self, pos_viewpoints, viewpoints_points, viewpoints_offense_points, citizen_vocality):
        sentence = ""
        sentence_beggining = True
        first_word = True
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


class Viewpoint:
    name = "Political View"

    pos_name = ""  # Positive, as in positive values.
    pos_words = []
    pos_offended_by = []

    neg_name = ""  # Negative, as in negative values.
    neg_words = []
    neg_offended_by = []

    def __init__(self):
        # self.value = 0 # This is how it's intended to be, but it's not so interesting.
        self.value = random.randrange(-100, 101)  # From 100(Left part of name) to -100(Right)
        self.stubborness = 1.0  # A rate at which we can change this view of the person.
        self.persuasiveness = 1.0  # A rate at which we can convince others of this view.

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


class Lib_Aut(Viewpoint):
    name = "Liberty-Authority"

    pos_name = "Liberty"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Liberty"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Liberty_Offensive"]

    neg_name = "Authority"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Authority"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Authority_Offensive"]


class Paci_Mili(Viewpoint):
    name = "Pacifism-Militarism"

    pos_name = "Pacifism"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Pacifism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Pacifism_Offensive"]

    neg_name = "Militarism"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Militarism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Militarism_Offensive"]


class Mat_Spi(Viewpoint):
    name = "Materialism-Spiritualism"

    pos_name = "Materialism"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Materialism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Materialism_Offensive"]

    neg_name = "Spiritualism"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Spiritualism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Spiritualism_Offensive"]


class Ind_Col(Viewpoint):
    name = "Individualism-Collectivism"

    pos_name = "Individualism"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Individualism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Individualism_Offensive"]

    neg_name = "Collectivism"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Collectivism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Collectivism_Offensive"]


class Ref_Rev(Viewpoint):
    name = "Reformism-Revolutionism"

    pos_name = "Reformism"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Reformism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Reformism_Offensive"]

    neg_name = "Revolutionism"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Revolutionism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Revolutionism_Offensive"]


class Ind_Pri(Viewpoint):
    name = "Industrialism-Primitivism"

    pos_name = "Industrialism"
    pos_words = LOCALE[LOCALE_LANGUAGE]["Industrialism"]
    pos_offended_by = LOCALE[LOCALE_LANGUAGE]["Industrialism_Offensive"]

    neg_name = "Primitivism"
    neg_words = LOCALE[LOCALE_LANGUAGE]["Primitivism"]
    neg_offended_by = LOCALE[LOCALE_LANGUAGE]["Primitivism_Offensive"]


class Faction:
    def __init_(self, leader):
        self.leader = leader
        self.members = [leader]

        self.political_view = leader.political_view


class Relationship:
    def __init__(self):
        # self.value = random.randrange(-100, 101)  # From 100(Left part of name) to -100(Right)
        self.value = 0  # We don't know anybody yet.

        self.permanent_min_val_modifier = 0  # Tweak this to allow this relationship to ever be worse.
        self.permanent_max_val_modifier = 0  # Tweak this to allow this relationship to be even better.

        self.title = LOCALE[LOCALE_LANGUAGE]["None"]  # Respect, like, dislike, hate.
        self.title_color = 'w'

    def adjust_value(self, us, target, value):
        """
        Adjusts self.value by value.
        Returns by how much we actually adjusted.
        """
        if(value < 0.1 and value > -0.1):
            return 0.0

        min_pos = self.get_min_possible(us, target)
        max_pos = self.get_max_possible(us, target)

        retVal = value

        self.value += round(retVal, 1)

        if(self.value > max_pos):
            retVal -= self.value - max_pos
            self.value = max_pos
        elif(self.value < min_pos):
            retVal -= self.value - min_pos
            self.value = min_pos

        return retVal


    def get_min_possible(self, us, target):
        """
        Gets minimum possible value of us disliking target.
        """
        retVal = CFG["DEFAULT_MIN_POSSIBLE_RELATIONSHIP_VALUE"] + self.permanent_min_val_modifier

        ideological_distance = 0
        axis_count = len(IDEOLOGIES_CLASSIFICATION[locale_to_original[us.ideology_name]]["Axis"])
        max_distance_per_axis = 200 ** 2

        max_possible_distance = axis_count * max_distance_per_axis

        for axis in IDEOLOGIES_CLASSIFICATION[locale_to_original[us.ideology_name]]["Axis"]:
            ideological_distance += (us.political_view.viewpoints[axis].value - target.political_view.viewpoints[axis].value) ** 2

        hate_from_ideology = translate(round(math.sqrt(ideological_distance), 1), 0, round(math.sqrt(max_possible_distance), 1), 0, -50) * (1.0 - us.tolerancy)

        retVal += hate_from_ideology

        retVal = round(retVal, 1)

        return clamp(retVal, -100.0, 100.0)

    def get_max_possible(self, us, target):
        """
        Gets maximum possible value of us liking target.
        """
        retVal = CFG["DEFAULT_MAX_POSSIBLE_RELATIONSHIP_VALUE"] + self.permanent_max_val_modifier
        if(us.ideology_name == target.ideology_name):
            retVal += 75
        else:
            ideological_distance = 0
            axis_count = len(IDEOLOGIES_CLASSIFICATION[locale_to_original[us.ideology_name]]["Axis"])
            max_distance_per_axis = 200 ** 2

            max_possible_distance = axis_count * max_distance_per_axis

            for axis in IDEOLOGIES_CLASSIFICATION[locale_to_original[us.ideology_name]]["Axis"]:
                ideological_distance += (us.political_view.viewpoints[axis].value - target.political_view.viewpoints[axis].value) ** 2

            love_from_ideology = translate(round(math.sqrt(ideological_distance), 1), 0, round(math.sqrt(max_possible_distance), 1), 50, 0)

            retVal += love_from_ideology

        retVal = round(retVal, 1)

        return clamp(retVal, -100.0, 100.0)


init_reference_lists()

citizens_to_spawn = 25
# citizens_to_spawn = 17
# citizens_to_spawn = 2
citizens_spawned = 0
citizens = []

from characters_presets import PRESET_CITIZENS

CITIZENS_TO_IMPORT = "All"  # Either "All", "None" or [citizen_name_to_import_1, citizen_name_to_import_2, ...]
# CITIZENS_TO_IMPORT = "None"
# CITIZENS_TO_IMPORT = ["UDaV73rus", "Ximik", "Artik12344", "Snailcat", "Garodil", "AnDan", "Akellazp", "BootManager", "Fukfuk", "DantezZz", "WallShrub", "Alweiss", "DctrMM", "DarkWater", "da_kiselev", "blind0", "Unbidden"]
# CITIZENS_TO_IMPORT = ["Luduk", "Co11y"]

if(CITIZENS_TO_IMPORT == "All"):
    for citizen_name in PRESET_CITIZENS:
        if(citizens_spawned >= citizens_to_spawn):
            break
        citizens.append(Citizen(citizen_name, PRESET_CITIZENS[citizen_name]))
        citizens_spawned += 1
elif(type(CITIZENS_TO_IMPORT) is list):
    for citizen_name in CITIZENS_TO_IMPORT:
        if(citizen_name not in PRESET_CITIZENS):
            continue
        if(citizens_spawned >= citizens_to_spawn):
            break
        citizens.append(Citizen(citizen_name, PRESET_CITIZENS[citizen_name]))
        citizens_spawned += 1

if(citizens_spawned < citizens_to_spawn):
    citizens_to_spawn -= citizens_spawned

    for i in range(citizens_to_spawn):
        citizens.append(Citizen("Random_Citizen_#" + str(i)))

"""
Server part.
"""

can_speak = False

def citizen_speech():
    global can_speak

    while(True):
        if(not can_speak):
            time.sleep(1)
            continue
        random.shuffle(citizens)
        for citizen in citizens:
            citizen.say()
            if(between_messages_delay_max > 0):
                if(between_messages_delay_min == between_messages_delay_max):
                    time.sleep(between_message_delay_min)
                else:
                    time.sleep(round(random.uniform(between_messages_delay_min, between_messages_delay_max), 1))


import threading

from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO

threading.Thread(target=citizen_speech).start()

if(CFG["IS_SERVER"]):
    ColorPrinter.to_style = "HTML"

    template_dir = os.path.abspath('../templates')
    static_dir = os.path.abspath('../static')

    app = Flask(__name__, template_folder=template_dir, static_url_path='')
    app.config['SECRET_KEY'] = CFG["SECRET_KEY"]
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    socketio = SocketIO(app)

    # Update cache if so required.
    if(CFG["UPDATE_CACHE"]):
        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

    @app.route('/')
    def sessions():
        return render_template("index.html")

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory(static_dir, path)

    @socketio.on('connection')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        global can_speak

        can_speak = True

        print("Received Connection from user(" + str(request.remote_addr) + "): " + str(json))
        socketio.emit('message', {"data": "Welcome."})

    @socketio.on('npc_message')
    def on_client_message(json, methods=['GET', 'POST']):
        message = json["data"]
        if(message == ""):
            return

        if(len(message) > 256):
            return

        socketio.emit('npc_message', json)

    @socketio.on('player_message')
    def on_client_message(json, methods=['GET', 'POST']):
        message = json["data"]
        if(message == ""):
            return

        if(len(message) > 256):
            return

        socketio.emit('player_message', json)

    socketio.run(app, host='0.0.0.0', port=CFG["PORT"], debug=CFG["DEBUG"])
else:
    can_speak = True

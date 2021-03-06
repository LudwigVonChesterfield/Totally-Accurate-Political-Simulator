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
import sys
import time
import random
import re
import math
import json

import global_vars

import config_loader
from config_loader import CONFIG_VALUES as CFG

from defines import *
from reactions import *

from locale_game import LOCALE
from ideologies_game import IDEOLOGIES_CLASSIFICATION

"""
Setting up CONFIG.
"""
CONFIG_REQUEST = {
    "DEBUG": {"cfg_type": "bool", "def_value": False},  # config_loader only outputs messages if this is True.

    "SECRET_KEY": {"cfg_type": "str", "def_value": "1111", "min_val": 1, "max_val": 100},  # This is not in the config.cfg, as it is always generated completely at random.
    "BACKDOOR_AUTHORIZATION_IP": {"cfg_type": "str", "def_value": "127.0.0.1", "min_val": 7, "max_val": 15},
    "BACKDOOR_AUTHORIZATION_WORD": {"cfg_type": "str", "def_value": "EINATH", "min_val": 1, "max_val": 100},
    "PORT": {"cfg_type": "int", "def_value": 8080, "min_val": 0, "max_val": 65535},
    "UPDATE_CACHE": {"cfg_type": "bool", "def_value": False},
    "MAX_PLAYER_COUNT": {"cfg_type": "int", "def_value": 30, "min_val": 0, "max_val": 100},
    "MAX_CLIENTS_PER_IP": {"cfg_type": "int", "def_value": 3, "min_val": 0, "max_val": 100},

    "DISCORD_OAUTH2_CLIENT_ID": {"cfg_type": "str", "def_value": "", "min_val": 0, "max_val": 100},
    "DISCORD_OAUTH2_CLIENT_SECRET": {"cfg_type": "str", "def_value": "", "min_val": 0, "max_val": 100},
    "DISCORD_OAUTH2_REDIRECT_URI": {"cfg_type": "str", "def_value": "", "min_val": 0, "max_val": 100},

    "LOCALE_LANGUAGE": {"cfg_type": "str", "def_value": "en", "min_val": 0, "max_val": 2, "possible_values": ["en", "ru", "la"]},

    "CITIZENS_TO_IMPORT": {"cfg_type": "list_or_str", "def_value": "All"},
    "CITIZENS_TO_SPAWN": {"cfg_type": "int", "def_value": 25, "min_val": 0, "max_val": 100},

    "MAX_WORDS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},
    "MAX_TARGETS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},
    "ALL_TARGETS_THRESHOLD": {"cfg_type": "int", "def_value": 5, "min_val": 1, "max_val": 30},
    "MAX_BOOK_SENTENCES": {"cfg_type": "int", "def_value": 20, "min_val": 1, "max_val": 30},

    "DEFAULT_RELATIONSHIP_SHIFT_VALUE": {"cfg_type": "float", "def_value": 2.0, "min_val": 0.0, "max_val": 100.0},
    "INITIAL_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": 0.0, "min_val": -100.0, "max_val": 100.0},

    "DEFAULT_MIN_POSSIBLE_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": -10.0, "min_val": -100.0, "max_val": 100.0},
    "DEFAULT_MAX_POSSIBLE_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": 10.0, "min_val": -100.0, "max_val": 100.0},

    "RELATIONSHIP_PERM_MODIFIER_ON_OFFENSE": {"cfg_type": "float", "def_value": 0.1, "min_val": -100.0, "max_val": 100.0},
    "RELATIONSHIP_PERM_MODIFIER_ON_CRIT_PERSUASION": {"cfg_type": "float", "def_value": 1.0, "min_val": -100.0, "max_val": 100.0},

    "DISLIKE_WORDS_MAXIMUM": {"cfg_type": "float", "def_value": 0.3, "min_val": 0.0, "max_val": 1.0},
    "DISLIKE_DELIMITERS_MAXIMUM": {"cfg_type": "float", "def_value": 0.3, "min_val": 0.0, "max_val": 1.0},
    "DISLIKE_UPPERCASE_MAXIMUM": {"cfg_type": "float", "def_value": 0.3, "min_val": 0.0, "max_val": 1.0},

    "DISLIKE_OFFENSES_MINIMUM": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 1.0},
    "OFFENSE_RELATIONSHIP_MULTIPLIER": {"cfg_type": "float", "def_value": 3.0, "min_val": -100.0, "max_val": 100.0},

    "DEFAULT_PERSUASION_MULTIPLIER": {"cfg_type": "float", "def_value": 2.0, "min_val": -100.0, "max_val": 100.0},
    "CRIT_PERSUASION_MULTIPLIER": {"cfg_type": "float", "def_value": 10.0, "min_val": -100.0, "max_val": 100.0},
    "CRIT_PERSUASION_DISLIKE_MULTIPLIER": {"cfg_type": "float", "def_value": 0.0, "min_val": -100.0, "max_val": 100.0},

    "CRIT_PERSUASION_STUBBORNESS_MODIFIER": {"cfg_type": "float", "def_value": 0.1, "min_val": 0.0, "max_val": 1.0},

    "MIN_EVENT_YEAR": {"cfg_type": "int", "def_value": 0, "min_val": 0, "max_val": 4000},
    "MAX_EVENT_YEAR": {"cfg_type": "int", "def_value": 2019, "min_val": 0, "max_val": 4000},

    "print_viewpoint_shifts": {"cfg_type": "bool", "def_value": True},
    "print_ideology_changes": {"cfg_type": "bool", "def_value": True},

    "print_relationship_shifts": {"cfg_type": "bool", "def_value": True},
    "print_relationship_changes": {"cfg_type": "bool", "def_value": True},

    "print_say_target": {"cfg_type": "bool", "def_value": True},

    "between_messages_delay_min": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 10.0},
    "between_messages_delay_max": {"cfg_type": "float", "def_value": 2.0, "min_val": 0.0, "max_val": 10.0},

    "between_reactions_delay_min": {"cfg_type": "float", "def_value": 0.1, "min_val": 0.0, "max_val": 10.0},
    "between_reactions_delay_max": {"cfg_type": "float", "def_value": 0.5, "min_val": 0.0, "max_val": 10.0}
}

config_loader.main(CONFIG_REQUEST)

# We import viewpoints here, since they are reliant on config_loader to parse data.
from viewpoint import *

"""
Global, constant variables.
"""
# See config_loader.py for more detail.
# See defines.py for more info too.

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

print_relationship_shifts = CFG["print_relationship_shifts"]  # Whether we print messages such as "changed their relation to: |^10.0|".
print_relationship_changes = CFG["print_relationship_changes"]  # Whether we print messages such as "A now hates B".

print_say_target = CFG["print_say_target"]  # Whether we print whom the message is adressed(If TRUE, messages will be of form: "A, B, C: I WANT TO SAY D").

# A delay between messages, if any.
between_messages_delay_min = CFG["between_messages_delay_min"]
between_messages_delay_max = CFG["between_messages_delay_max"]

# A delay between reactions, if any.
between_reactions_delay_min = CFG["between_reactions_delay_min"]
between_reactions_delay_max = CFG["between_reactions_delay_max"]

RELATIONSHIP_THRESHOLDS = [
    {"Name": "Reverence", "Min": 90, "Max": 100, "Color": 'green; font-weight: bold', "Reaction_Mod": 90},
    {"Name": "Respect", "Min": 50, "Max": 90, "Color": 'green', "Reaction_Mod": 50},
    {"Name": "Sympathy", "Min": 25, "Max": 50, "Color": 'white', "Reaction_Mod": 25},
    {"Name": "Distaste", "Min": -50, "Max": -25, "Color": 'white', "Reaction_Mod": -25},
    {"Name": "Hate", "Min": -90, "Max": -50, "Color": 'red', "Reaction_Mod": -50},
    {"Name": "Feud", "Min": -100, "Max": -90, "Color": 'red; font-weight: bold', "Reaction_Mod": -90}
]

"""
Lambda functions and functions.
"""
from savefiles import save_state, load_state

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

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
    return random.choice(closest_approximations[min(closest_approximations.keys(), key=float)])

def init_viewpoints_by_words_list():
    pos_viewpoints = get_all_subclasses(Viewpoint)
    for viewpoint in pos_viewpoints:
        for word in viewpoint.pos_words:
            global_vars.viewpoints_by_word[word] = {"Viewpoint": viewpoint.name, "Value": 1}
        for word in viewpoint.neg_words:
            global_vars.viewpoints_by_word[word] = {"Viewpoint": viewpoint.name, "Value": -1}

        for word in viewpoint.pos_offended_by:
            global_vars.offensive_to_viewpoint[word] = {"Viewpoint": viewpoint.name, "Value": 1}
        for word in viewpoint.neg_offended_by:
            global_vars.offensive_to_viewpoint[word] = {"Viewpoint": viewpoint.name, "Value": -1}

def init_locale_relate_original():
    for original_item, locale_item in LOCALE[LOCALE_LANGUAGE].items():
        if(type(locale_item) is list):
            continue
            """

            If you want to reference the pairs of word and their translations in lists such as EN_PRIMITIVISM_WORDS you'd need to rework all of this.

            for locale_item_in_list in locale_item:
                locale_to_original
            """
        global_vars.locale_to_original[locale_item] = original_item
        global_vars.original_to_locale[original_item] = locale_item

def init_reference_lists():
    init_viewpoints_by_words_list()
    init_locale_relate_original()


def init_citizens():
    if(load_state("last")):
        return

    citizens_to_spawn = CFG["CITIZENS_TO_SPAWN"]
    citizens_spawned = 0

    exists = os.path.isfile("./characters_presets.json")
    if exists:
        with open("./characters_presets.json") as PRESET_FILE:
            PRESET_CITIZENS = json.load(PRESET_FILE)

            CITIZENS_TO_IMPORT = CFG["CITIZENS_TO_IMPORT"]

            if(CITIZENS_TO_IMPORT == "All"):
                for citizen_saveObject in PRESET_CITIZENS:
                    if(citizens_spawned >= citizens_to_spawn):
                        break
                    global_vars.citizens.append(Citizen(citizen_saveObject["name"], citizen_saveObject))
                    citizens_spawned += 1

            elif(type(CITIZENS_TO_IMPORT) is list):
                for citizen_saveObject in PRESET_CITIZENS:
                    if(citizen_saveObject["name"] not in CITIZENS_TO_IMPORT):
                        continue
                    if(citizens_spawned >= citizens_to_spawn):
                        break

                    global_vars.citizens.append(Citizen(citizen_saveOBject["name"], citizen_saveObject))
                    citizens_spawned += 1

    if(citizens_spawned < citizens_to_spawn):
        citizens_to_spawn -= citizens_spawned

        for i in range(citizens_to_spawn):
            # global_vars.citizens.append(Citizen("Random_Citizen_#" + str(i)))
            global_vars.citizens.append(Citizen(random.choice(POS_NAMES) + "_" + random.choice(POS_SURNAMES)))

    global_vars.citizens.append(Player("Player"))


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


def generate_reaction(emotionality, possible_trigger, speaker=True, saveObject={}):
    """
    speaker - is how we react to somebody expressing emotion.
    speaker false - is how we react to somebody who provoked an emotion in somebody else.
    """
    trigger_happiness = 0
    list_to_search = "reactions_speaker"
    if(not speaker):
        list_to_search = "reactions_provoker"

    if(list_to_search in saveObject.keys() and str(possible_trigger) in saveObject[list_to_search].keys()):
        return str_to_class(saveObject[list_to_search][str(possible_trigger)]["type"]).load_save_state(saveObject[list_to_search][str(possible_trigger)])

    trigger_hapiness = random.uniform(-1.0, 1.0)
    reaction_class = random.choice(get_all_subclasses(Reaction))
    return reaction_class(emotionality, trigger_hapiness)


def to_chat(text):
    for ip_client_info in global_vars.client_infos_by_ip.values():
        for client_info in ip_client_info:
            if(client_info.loaded):
                client_info.saved_messages.append(text)

    speak_to = list(global_vars.clients_by_sid.values()).copy()
    for client in speak_to:
        if(not client.disconnecting):
            client.whisper(text)


def to_chat_relationship_shift(listener, speaker, value):
    if((value > 0.1 or value < -0.1) and print_relationship_shifts):
        shift_sign = sign(value)

        arrow_indicator = ''
        color_indicator = ''

        if(shift_sign > 0.0):
            arrow_indicator = UP_ARROW_SYMBOL
            color_indicator = 'green'
        else:
            arrow_indicator = DOWN_ARROW_SYMBOL
            color_indicator = 'red'

        relationship_string = "<span class='ui_element'>|</span>"
        relationship_string += "<span style='color: " + color_indicator + "'>" + arrow_indicator + str(round(value, 1)) + "</span>"
        relationship_string += "<span class='ui_element'>|</span>"

        to_chat("<span class='emote_name'>" + listener.name + "</span>" +
                "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Relationship Changed To"] + " </span>" +
                "<span class='emote_name'>" + speaker.name + "</span>" +
                "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + " </span> " +
                relationship_string)


class Citizen:
    def __init__(self, name, saveObject={}):
        saveObject_keys = saveObject.keys()
        if("name" in saveObject_keys):
            name = saveObject["name"]

        while(name.lower() in global_vars.taken_clean_citizen_names):
            name = name + random.choice(NAME_LETTERS)

        global_vars.taken_clean_citizen_names.append(name.lower())

        if("age" in saveObject_keys):
            self.age = saveObject["age"]
        else:
            self.age = 1

        self.name = name

        if("vocal" in saveObject_keys):
            self.vocal = saveObject["vocal"]
        else:
            self.vocal = random.uniform(0.0, 1.0)  # How vocal we are about our opinions. Where 0 is not vocal at all, and 1 is very vocal.

        if("tolerancy" in saveObject_keys):
            self.tolerancy = saveObject["tolerancy"]
        else:
            self.tolerancy = random.uniform(0.0, 1.0)  # How hard we hate people with other ideologies, and how often we try to offend them.

        if("political_view" in saveObject_keys):
            self.political_view = View.load_save_state(saveObject["political_view"])
        else:
            self.political_view = View()

        if("emotions" in saveObject_keys):
            self.emotions = Emotions.load_save_state(saveObject["emotions"])
        else:
            self.emotions = Emotions()

        self.ideology_name = get_closest_ideology(self.political_view.generate_political_axis())

        if("favour_words" in saveObject_keys):
            self.favour_words = saveObject["favour_words"]
        else:
            self.favour_words = {}
        if("dislike_words" in saveObject_keys):
            self.dislike_words = saveObject["dislike_words"]
        else:
            self.dislike_words = {}
        self.generate_words_relation()

        if("favour_intonations" in saveObject_keys):
            self.favour_intonations = saveObject["favour_intonations"]
        else:     
            self.favour_intonations = {}
        if("dislike_intonations" in saveObject_keys):
            self.dislike_intonations = saveObject["dislike_intonations"]
        else:
            self.dislike_intonations = {}
        self.generate_intonations_relation()

        if("favour_word_uppercase" in saveObject_keys):
            self.favour_word_uppercase = saveObject["favour_word_uppercase"]
        else:
            self.favour_word_uppercase = {}
        if("dislike_word_uppercase" in saveObject_keys):
            self.dislike_word_uppercase = saveObject["dislike_word_uppercase"]
        else:
            self.dislike_word_uppercase = {}
        self.generate_uppercase_relation()

        """
        if("to_quote" in saveObject_keys):
            self.to_quote = saveObject["to_quote"]
        else:
            self.to_quote = []  # Things this very citizen would like to quote in the future, whenever they can.
        """
        self.to_quote = []  # Things this very citizen would like to quote in the future, whenever they can.

        self.relationships = {}
        if("relationships" in saveObject_keys):
            for citizen_name in saveObject["relationships"].keys():
                self.relationships[citizen_name] = Relationship.load_save_state(saveObject["relationships"][citizen_name])
                self.update_relationship_title(citizen_name)

        for citizen in global_vars.citizens:
            if(citizen.name not in self.relationships.keys()):
                self.relationships[citizen.name] = Relationship()
                self.adjust_relationship_value(citizen, CFG["INITIAL_RELATIONSHIP_VALUE"])
                self.update_relationship_title(citizen.name)
            if(self.name not in citizen.relationships.keys()):
                citizen.relationships[self.name] = Relationship()
                citizen.adjust_relationship_value(self, CFG["INITIAL_RELATIONSHIP_VALUE"])
                citizen.update_relationship_title(self.name)

        self.inventory = []
        if("inventory" in saveObject_keys):
            for item in saveObject["inventory"]:
                str_to_class(item["type"]).load_save_state(item)

    def generate_words_relation(self):
        for word in global_vars.viewpoints_by_word:
            if(word not in self.favour_words):
                self.favour_words[word] = random.uniform(0.0, 1.0)  # How much we like this word(it may persuade us more). Where 0 is we don't like it at all, 1 is we like the word very much.
            if(word not in self.dislike_words):
                self.dislike_words[word] = random.uniform(0.0, CFG["DISLIKE_WORDS_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

        for offense in global_vars.offensive_to_viewpoint.keys():
            if(offense not in self.favour_words):
                self.favour_words[offense] = 0.0
            if(offense not in self.dislike_words):
                self.dislike_words[offense] = random.uniform(CFG["DISLIKE_OFFENSES_MINIMUM"], 1.0)

        all_word = LOCALE[LOCALE_LANGUAGE]["All"].lower()
        if(all_word not in self.favour_words):
            self.favour_words[all_word] = random.uniform(0.0, 1.0)
        if(all_word not in self.dislike_words):
            self.dislike_words[all_word] = 0.0

        clean_name = self.name.lower()

        if(clean_name not in self.favour_words):
            self.favour_words[clean_name] = random.uniform(0.0, 1.0)
        if(clean_name not in self.dislike_words):
            self.dislike_words[clean_name] = 0.0
        for citizen in global_vars.citizens:
            if(clean_name not in citizen.favour_words):
                citizen.favour_words[clean_name] = random.uniform(0.0, 1.0)
            if(clean_name not in citizen.dislike_words):
                citizen.dislike_words[clean_name] = 0.0

            clean_citizen_name = citizen.name.lower()

            if(clean_citizen_name not in self.favour_words):
                self.favour_words[clean_citizen_name] = random.uniform(0.0, 1.0)
            if(clean_citizen_name not in self.dislike_words):
                self.dislike_words[clean_citizen_name] = 0.0

    def generate_intonations_relation(self):
        for intonation in DELIMETERS_SENTENCE_END:
            if(intonation not in self.favour_intonations):
                self.favour_intonations[intonation] = random.uniform(0.0, 1.0)  # How much we like this intonation. Where 0 is we don't like it at all, 1 is we like the word very much.
            if(intonation not in self.dislike_intonations):
                self.dislike_intonations[intonation] = random.uniform(0.0, CFG["DISLIKE_DELIMITERS_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

    def generate_uppercase_relation(self):
        for word_uppercase in WORD_UPPERCASE_POSSIBILITIES:
            if(word_uppercase not in self.favour_word_uppercase):
                self.favour_word_uppercase[word_uppercase] = random.uniform(0.0, 1.0)  # How much we like when the word is shouted, or said with uppercase. Where 0 is we don't like it at all, 1 is we like the word very much.
            if(word_uppercase not in self.dislike_word_uppercase):
                self.dislike_word_uppercase[word_uppercase] = random.uniform(0.0, CFG["DISLIKE_UPPERCASE_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

    def get_targets(self, predetermined_targets=None):
        targets_amount = 0
        targets = []
        if(type(predetermined_targets) is not list):
            targets_amount = round(CFG["MAX_TARGETS"] * random.uniform(0.0, self.vocal))
            if(targets_amount == 0):
                return {"targets_amount": targets_amount, "targets": targets}

            for t in range(targets_amount):
                new_target = random.choice(global_vars.citizens)
                if(new_target in targets):  # We are already shouting to them.
                    continue
                if(new_target == self):  # Don't talk to yourself... TODO: Add instanity.
                    continue

                targets.append(new_target)
        else:
            targets_amount = len(predetermined_targets)
            targets = predetermined_targets
        return {"targets_amount": targets_amount, "targets": targets}

    def get_targets_text(self, targets_amount, targets):
        targets_text = ""
        if(targets_amount > CFG["ALL_TARGETS_THRESHOLD"]):
            all_word = LOCALE[LOCALE_LANGUAGE]["All"]
            if(prob((self.vocal * self.emotions.emotionality) * 100)):
                all_word = all_word.upper()
            else:
                all_word = all_word.capitalize()

            targets_text = all_word + ", "
        else:
            first_target = True

            for new_target in targets:
                if(not first_target):
                    targets_text += ", "
                first_target = False
                new_target_name = new_target.name
                if(prob((self.vocal * self.emotions.emotionality) * 100)):
                    new_target_name = new_target_name.upper()

                targets_text += new_target_name
            if(not first_target):
                targets_text += ", "
        return targets_text

    def get_sentence(self, targets, targets_text, words_amount, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan'):
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
                    is_offensive = predetermined_triggers & MESSAGE_TRIGGER_OFFENSIVE
                    for target in targets:
                        if(self.offend_target_prob(target, viewpoint) or is_offensive):
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

        return self.political_view.get_sentence(pos_viewpoints, viewpoints_points, viewpoints_offense_points, self.vocal, targets_text)

    def queue_say(self, verb=None, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan', on_say_done=None, on_say_done_args=None):
        global_vars.actions_queue.append(
            {
                "speaker": self,
                "verb": verb,
                "type": "say",
                "predetermined_targets": predetermined_targets,
                "predetermined_triggers": predetermined_triggers,
                "fg_color": fg_color,
                "bg_color": bg_color,
                "on_say_done": on_say_done,
                "on_say_done_args": on_say_done_args
            })

    def say(self, verb=None, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan', on_say_done=None, on_say_done_args=None):
        """
        Returns False if we didn't say anything.
        Returns True if we did say something.
        """
        if(between_messages_delay_max > 0):
            if(between_messages_delay_min == between_messages_delay_max):
                time.sleep(between_message_delay_min)
            else:
                time.sleep(round(random.uniform(between_messages_delay_min, between_messages_delay_max), 1))

        words_amount = round(CFG["MAX_WORDS"] * random.uniform(0.0, self.vocal))
        if(words_amount == 0):
            return False

        targets_object = self.get_targets(predetermined_targets)
        targets_amount = targets_object["targets_amount"]
        targets = targets_object["targets"]

        targets_text = self.get_targets_text(targets_amount, targets)

        sentence = self.get_sentence(targets, targets_text, words_amount, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan')
        if(verb is None):
            verb = self.get_verb(sentence)
        else:
            verb = LOCALE[LOCALE_LANGUAGE][verb]

        if(len(sentence) == 0):
            sentence = "..."

        print_sentence = sentence
        sentence = targets_text + sentence
        if(print_say_target):
            print_sentence = targets_text + print_sentence

        my_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
        my_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

        to_chat("<span class='speech_name'>" + self.name + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>(</span>" +
                "<span style='color: " + my_ideology_fg + "'>" + LOCALE[LOCALE_LANGUAGE][self.ideology_name] + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>)</span>" +
                "<span class='speech_verb'> " + verb + ", </span>" +
                "<span class='speech_wrapper'><span style='color: " + bg_color + "'>\"</span></span>" +
                "<span style='color: " + fg_color + "'>" + print_sentence + "</span>" +
                "<span class='speech_wrapper'><span style='color: " + bg_color + "'>\"</span></span>")

        to_hear = global_vars.citizens.copy()
        to_hear.remove(self)
        random.shuffle(to_hear)

        for citizen in to_hear:
            citizen.queue_hear(self, verb, sentence, predetermined_triggers)

        if(on_say_done is not None):
            on_say_done(on_say_done_args)

        return True

    def queue_hear(self, speaker, verb, sentence, predetermined_triggers, proxy_speaker=None, on_hear_done=None, on_hear_done_args=None):
        global_vars.reactions_queue.appendleft(
            {
                "hearer": self,
                "type": "hear",
                "speaker": speaker,
                "verb": verb,
                "sentence": sentence,
                "predetermined_triggers": predetermined_triggers,
                "proxy_speaker": proxy_speaker,
                "on_hear_done": on_hear_done,
                "on_hear_done_args": on_hear_done_args
            })

    def hear(self, speaker, verb, sentence, predetermined_triggers, proxy_speaker=None, on_hear_done=None, on_hear_done_args=None):
        """
        speaker is who said the sentence.
        proxy_speaker is used in quoting, it's the original author of the quote. We change relationship to him, and to speaker.
        """
        message_triggers = predetermined_triggers

        intonation_delimeter = sentence[len(sentence) - 1]

        delimeters_to_remove = "[" + "".join(DELIMETERS) + "]"
        sentence_stripped = re.sub(delimeters_to_remove, "", sentence)
        sentence_stripped = sentence_stripped.strip()  # Remove trailing spaces.
        words = []
        if(len(sentence_stripped) > 0):
            words = sentence_stripped.split(" ")

        can_hear = False

        if(self.relationships[speaker.name].title in ["Reverence", "Feud"]):  # We listen to our friends, and to enemies.
            if(self.listen_to_speaker_check(speaker, None, verb, sentence)):
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
                if(clean_word in global_vars.offensive_to_viewpoint.keys()):
                    point = global_vars.offensive_to_viewpoint[clean_word]["Viewpoint"]
                    point_value = self.political_view.viewpoints[point].value

                    # If they said something offensive, check if we hear them!
                    if(sign(point_value) == sign(global_vars.offensive_to_viewpoint[clean_word]["Value"]) and self.listen_to_speaker_check(speaker, word, verb, sentence)):
                        can_hear = True
                        break

                if(clean_word == self.name.lower() or clean_word == clean_all_word):
                    if(self.listen_to_speaker_check(speaker, word, verb, sentence)):
                        can_hear = True
                        break

                to_check -= 1

        if(not can_hear or len(words) == 0):
            return

        if(between_reactions_delay_max > 0):
            if(between_reactions_delay_min == between_reactions_delay_max):
                time.sleep(between_reactions_delay_min)
            else:
                time.sleep(round(random.uniform(between_reactions_delay_min, between_reactions_delay_max), 1))

        shifted_viewpoints = {}
        relationship_shift = 0
        proxy_relationship_shift = 0
        for word in words:
            retVal = self.react_word(speaker, verb, intonation_delimeter, word, proxy_speaker)
            if(retVal["Viewpoint"] != ""):
                if(retVal["Viewpoint"] in shifted_viewpoints):
                    shifted_viewpoints[retVal["Viewpoint"]] += retVal["Viewpoint_Shift_Value"]
                else:
                    shifted_viewpoints[retVal["Viewpoint"]] = retVal["Viewpoint_Shift_Value"]
            relationship_shift += retVal["Relationship_Shift_Value"]
            message_triggers = message_triggers | retVal["Message_Triggers"]

        if(message_triggers & MESSAGE_TRIGGER_PERSUASIVE):
            to_see_persuade = global_vars.citizens.copy()
            to_see_persuade.remove(self)
            to_see_persuade.remove(speaker)
            random.shuffle(to_see_persuade)

            for citizen in to_see_persuade:
                citizen.queue_hear_emote(self, None, speaker, predetermined_triggers=message_triggers)

        shift_occured = False
        convinced_string = "<span class='ui_element'>|</span>"

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
                arrow_indicator = LEFT_ARROW_SYMBOL
                color_indicator = self.political_view.viewpoints[viewpoint_shift].pos_color
            else:
                arrow_indicator = RIGHT_ARROW_SYMBOL
                color_indicator = self.political_view.viewpoints[viewpoint_shift].neg_color

            convinced_string += "<span style='color: " + color_indicator + "'>" + letters + arrow_indicator + str(abs(round(retVal, 1))) + "</span>"
            convinced_string += "<span class='ui_element'>|</span>"

        if(shift_occured):
            self.ideology_name = get_closest_ideology(self.political_view.generate_political_axis())

            if(print_viewpoint_shifts):
                to_chat("<span class='emote_name'>" + speaker.name + "</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Convinced"] + " </span>" +
                        "<span class='emote_name'>" + self.name + "</span>" +
                        "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + " </span>" +
                        convinced_string)
            if(print_ideology_changes and old_ideology_name != self.ideology_name):
                old_ideology_fg = IDEOLOGIES_CLASSIFICATION[old_ideology_name]["Foreground"]
                old_ideology_bg = IDEOLOGIES_CLASSIFICATION[old_ideology_name]["Background"]
                new_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
                new_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

                to_chat("<span class='emote_name'>" + self.name + "</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Changed Ideology From"] + ": </span>" +
                        "<span style='color: " + old_ideology_bg + "'>(</span>" +
                        "<span style='color: " + old_ideology_fg + "'>" + LOCALE[LOCALE_LANGUAGE][old_ideology_name] + "</span>" +
                        "<span style='color: " + old_ideology_bg + "'>)</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["To"] + ": </span>" +
                        "<span style='color: " + new_ideology_bg + "'>(</span>" +
                        "<span style='color: " + new_ideology_fg + "'>" + LOCALE[LOCALE_LANGUAGE][self.ideology_name] + "</span>" +
                        "<span style='color: " + new_ideology_bg + "'>)</span>" +
                        "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"])

        self.shift_relationships_and_print([speaker, relationship_shift])
        if(proxy_speaker and proxy_speaker != self and proxy_speaker != speaker):
            self.shift_relationships_and_print([proxy_speaker, relationship_shift])

        interupt_reply = False
        if(prob(self.emotions.emotionality * 100)):
            interupt_reply = self.emotions.react_to_triggers(self, speaker, None, message_triggers, text=sentence)  # Nobody provoked us to speak, thus None as provoker.     
        if(not interupt_reply):
            self.queue_say(predetermined_targets=[speaker])

        if(on_hear_done is not None):
            on_hear_done(on_hear_done_args)

    def react_word(self, speaker, verb, intonation_delimeter, word, proxy_speaker=None):
        """
        How self reacts to speaker's word.
        Returns what viewpoint changed, and by how much in format {"Viewpoint": viewpoint_name, "Value": value_changed}.
        """
        # Currently used to determine which emotions this or that message can provoke. See define.py.
        message_triggers = MESSAGE_TRIGGER_NONE

        """
        Favour is how critically persuasive the word is.
        Dislike is how much we didn't like it.
        """
        clean_word = word.lower()
        if(clean_word in global_vars.viewpoints_by_word.keys()):
            base_value = global_vars.viewpoints_by_word[clean_word]["Value"] * CFG["DEFAULT_PERSUASION_MULTIPLIER"]
            favour = self.favour_words[clean_word] * self.favour_intonations[intonation_delimeter]
        else:  # It's either a filler, or something offensive.
            base_value = 0.0
            favour = 0.0

        relationship_value = CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"]
        dislike = 0

        if(clean_word in global_vars.offensive_to_viewpoint.keys()):
            point_name = global_vars.offensive_to_viewpoint[clean_word]["Viewpoint"]
            if(sign(self.political_view.viewpoints[point_name].value) == sign(global_vars.offensive_to_viewpoint[clean_word]["Value"])):
                dislike = (self.dislike_words[clean_word] + self.dislike_intonations[intonation_delimeter]) * 0.5  # We don't care how offensive the word is if it's not offensive.
                relationship_value *= CFG["OFFENSE_RELATIONSHIP_MULTIPLIER"]  # If it's an offense, it's safe to assume that it'll become negative afterwards.

                self.relationships[speaker.name].permanent_min_val_modifier -= CFG["RELATIONSHIP_PERM_MODIFIER_ON_OFFENSE"]
                self.relationships[speaker.name].permanent_max_val_modifier -= CFG["RELATIONSHIP_PERM_MODIFIER_ON_OFFENSE"]

                message_triggers = message_triggers | MESSAGE_TRIGGER_OFFENSIVE

        if(word.isupper()):
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_UPPER]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_UPPER]) * 0.5  # We do care that we are shouted at.
            message_triggers = message_triggers | MESSAGE_TRIGGER_SHOUT
        elif(word[0].isupper()):  # Checks if capitalized.
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_CAPITALIZE]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_CAPITALIZE]) * 0.5
        else:
            favour *= self.favour_word_uppercase[WORD_UPPERCASE_NONE]
            dislike = (dislike + self.dislike_word_uppercase[WORD_UPPERCASE_NONE]) * 0.5

        viewpoint_name = ""
        if(clean_word in global_vars.viewpoints_by_word.keys()):
            viewpoint_name = global_vars.viewpoints_by_word[clean_word]["Viewpoint"]

            base_value *= (1.0 - self.get_stubborness(viewpoint_name)) * speaker.get_persuasiveness(viewpoint_name)

            favour *= (self.relationships[speaker.name].value + 100) / 200  # If we dislike them as a person they have a lower chance to persuade us.

            if(self.crit_persuaded_prob(speaker, viewpoint_name, favour)):
                dislike *= CFG["CRIT_PERSUASION_DISLIKE_MULTIPLIER"]  # We were very much persuaded. We do not hate this person at all.

                self.relationships[speaker.name].permanent_min_val_modifier += CFG["RELATIONSHIP_PERM_MODIFIER_ON_CRIT_PERSUASION"]
                self.relationships[speaker.name].permanent_max_val_modifier += CFG["RELATIONSHIP_PERM_MODIFIER_ON_CRIT_PERSUASION"]

                base_value *= CFG["CRIT_PERSUASION_MULTIPLIER"]

                # If our viewpoint is of same value as of person's who persuaded us, we gain a convincing argument which strengthens our stubborness.
                # Otherwise, we become somewhat less stubborn.
                if(sign(self.political_view.viewpoints[viewpoint_name].value) == sign(global_vars.viewpoints_by_word[clean_word]["Value"])):
                   self.political_view.viewpoints[viewpoint_name].stubborness += CFG["CRIT_PERSUASION_STUBBORNESS_MODIFIER"]
                else:
                   self.political_view.viewpoints[viewpoint_name].stubborness -= CFG["CRIT_PERSUASION_STUBBORNESS_MODIFIER"]

                message_triggers = message_triggers | MESSAGE_TRIGGER_PERSUASIVE

        base_value *= (1.0 - dislike)

        relationship_value *= favour - dislike

        return {"Viewpoint": viewpoint_name, "Viewpoint_Shift_Value": base_value, "Relationship_Shift_Value": relationship_value, "Message_Triggers": message_triggers}

    def queue_emote(self, emotion, emotion_target=None, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, on_emote_done=None, on_emote_done_args=None):
        global_vars.actions_queue.append(
            {
                "speaker": self,
                "type": "emote",
                "emotion": emotion,
                "emotion_target": emotion_target,
                "predetermined_targets": predetermined_targets,
                "predetermined_triggers": predetermined_triggers,
                "on_emote_done": on_emote_done,
                "on_emote_done_args": on_emote_done_args,
            })

    def emote(self, emotion, emotion_target=None, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, on_emote_done=None, on_emote_done_args=None):
        """
        emote_target is used in messages to determine whom the emote is directed at, if anybody.
        predetermined_targets is who will hear_emote this emote.
        predetermined_triggers is used for emotional replies.
        """
        if(between_reactions_delay_max > 0):
            if(between_reactions_delay_min == between_reactions_delay_max):
                time.sleep(between_reactions_delay_min)
            else:
                time.sleep(round(random.uniform(between_reactions_delay_min, between_reactions_delay_max), 1))

        targets_amount = 0
        targets = []
        if(type(predetermined_targets) is not list):
            targets_amount = round(CFG["MAX_TARGETS"] * random.uniform(0.0, self.emotions.emotionality))
            if(targets_amount == 0):
                return

            for t in range(targets_amount):
                new_target = random.choice(global_vars.citizens)
                if(new_target in targets):  # We are already shouting to them.
                    continue
                if(new_target == self):  # Don't talk to yourself... TODO: Add insanity.
                    continue

                targets.append(new_target)
        else:
            targets_amount = len(predetermined_targets)
            targets = predetermined_targets

        emotion_target_text = ""
        if(emotion_target):
            emotion_target_text = " " + "</span><span class='speech_name'>" + emotion_target.name + "</span><span class='speech_verb'>"

        # For some reason we denote these as speech. It's somewhat intentional.
        to_chat("<span class='speech_name'>" + self.name + "</span>" +
                "<span class='speech_verb'> " + LOCALE[LOCALE_LANGUAGE][emotion + ("_target" if emotion_target else "")] + emotion_target_text + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")

        to_hear_emote = targets
        random.shuffle(to_hear_emote)

        for citizen in to_hear_emote:
            emotion_target_name = "None"
            if(emotion_target):
                emotion_target_name = emotion_target.name
            citizen.queue_hear_emote(self, emotion, emotion_target, predetermined_triggers)

        if(on_emote_done is not None):
            on_emote_done(on_emote_done_args)

    def queue_hear_emote(self, speaker, emotion, provoker, predetermined_triggers=MESSAGE_TRIGGER_NONE):
        global_vars.reactions_queue.appendleft(
            {
                "hearer": self,
                "type": "hear_emote",
                "speaker": speaker,
                "emotion": emotion,
                "provoker": provoker,
                "predetermined_triggers": predetermined_triggers,
            })

    def hear_emote(self, speaker, emotion, provoker, predetermined_triggers):
        if(not prob(self.emotions.emotionality * 100 - 1)):
            return

        if(between_reactions_delay_max > 0):
            if(between_reactions_delay_min == between_reactions_delay_max):
                time.sleep(between_reactions_delay_min)
            else:
                time.sleep(round(random.uniform(between_reactions_delay_min, between_reactions_delay_max), 1))

        interupt_reply = False
        if(prob(self.emotions.emotionality * 100)):
            interupt_reply = self.emotions.react_to_triggers(self, speaker, provoker, predetermined_triggers)
        if(not interupt_reply):
            reply_to = [speaker]
            if(provoker and provoker != self):
                reply_to.append(provoker)
            self.queue_say(predetermined_targets=reply_to)

    def write_book(self, stubborness, predetermined_targets=[]):
        sentences = round(CFG["MAX_BOOK_SENTENCES"] * random.uniform(0.0, stubborness))
        if(sentences == 0.0):
            return None

        my_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
        my_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

        book_text = ""
        first_sentence = True
        for i in range(sentences - 1):
            words_amount = round(CFG["MAX_WORDS"] * random.uniform(0.0, stubborness))
            if(words_amount == 0):
                continue
            new_words = self.get_sentence(predetermined_targets, "", words_amount, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color=my_ideology_fg, bg_color=my_ideology_bg)
            if(new_words == ""):
                continue
            starts_with = " "
            if(first_sentence):
                starts_with = ""
                first_sentence = False
            book_text += starts_with + new_words

        if(book_text == ""):
            return None

        if(len(predetermined_targets) > 0):
            targets_text = self.get_targets_text(len(predetermined_targets), predetermined_targets)
            if(len(targets_text) > 2):
                targets_text = targets_text[:-2]
                targets_text += "."
            book_text += " " + targets_text

        book_title = str("<span style='color: " + my_ideology_bg + "'>\"</span>" +
                     "<span style='color: " + my_ideology_fg + "'>" +
                     random.choice(LOCALE[LOCALE_LANGUAGE]["Book_Titles"]) % (LOCALE[LOCALE_LANGUAGE][self.ideology_name]) +
                     "</span>" +
                     "<span style='color: " + my_ideology_bg + "'>\"</span>")

        to_chat("<span class='emote_name'>" + self.name + "</span>" +
                "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Writes"] + " </span>" +
                book_title +
                "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")

        print(self.name, book_title)
        print(book_text)
        book = Book(self, book_title, book_text)
        book.pickup(self)
        return book

    def read_book(self, args):
        book = args["book"]
        predetermined_triggers = args["predetermined_triggers"]
        sentence = book.text

        my_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
        my_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

        if(args["quote"]):
            self.quote(book.created_by, sentence, verb=LOCALE[LOCALE_LANGUAGE]["Quotes"] + " " + book.name,
                       predetermined_triggers=predetermined_triggers, fg_color=my_ideology_fg, bg_color=my_ideology_bg)
        else:
            verb = LOCALE[LOCALE_LANGUAGE]["Reads"] + " " + book.name

            to_chat("<span class='speech_name'>" + self.name + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>(</span>" +
                "<span style='color: " + my_ideology_fg + "'>" + LOCALE[LOCALE_LANGUAGE][self.ideology_name] + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>)</span>" +
                "<span class='speech_verb'> " + verb + ", </span>" +
                "<span class='speech_wrapper'><span style='color: " + my_ideology_bg + "'>\"</span></span>" +
                "<span style='color: " + my_ideology_fg + "'>" + sentence + "</span>" +
                "<span class='speech_wrapper'><span style='color: " + my_ideology_bg + "'>\"</span></span>")

            to_hear = global_vars.citizens.copy()
            to_hear.remove(self)
            random.shuffle(to_hear)

            for citizen in to_hear:
                if(book.can_use(self, citizen)):
                    citizen.queue_hear(self, verb, sentence, predetermined_triggers,
                                       proxy_speaker=book.created_by,
                                       on_hear_done=book.read_by_names.append,
                                       on_hear_done_args=citizen)

        return True

    def quote(self, speaker, sentence, verb=None, predetermined_targets=[], predetermined_triggers=MESSAGE_TRIGGER_QUOTE, fg_color='white', bg_color='cyan'):
        """
        Strips all the words we do not agree with from sentence, and then says them.
        """
        delimeters_to_remove = "[" + "".join(DELIMETERS) + "]"
        sentence_stripped = re.sub(delimeters_to_remove, "", sentence)
        sentence_stripped = sentence_stripped.strip()  # Remove trailing spaces.
        words = []
        new_words = []

        if(len(sentence_stripped) > 0):
            words = sentence.split(" ")

        first_word = True

        for word in words:
            word_stripped = re.sub(delimeters_to_remove, "", word)
            word_stripped = word_stripped.strip()  # Remove trailing spaces.

            if(len(word_stripped) <= 0):
                continue

            clean_word = word_stripped.lower()
            if(clean_word in global_vars.taken_clean_citizen_names):
                continue
            if(clean_word == LOCALE[LOCALE_LANGUAGE]["All"].lower()):
                continue

            if(clean_word in global_vars.viewpoints_by_word.keys() and (sign(self.political_view.viewpoints[global_vars.viewpoints_by_word[clean_word]["Viewpoint"]].value) != sign(global_vars.viewpoints_by_word[clean_word]["Value"]))):
                continue

            if(clean_word in global_vars.offensive_to_viewpoint.keys() and (sign(self.political_view.viewpoints[global_vars.offensive_to_viewpoint[clean_word]["Viewpoint"]].value) == sign(global_vars.offensive_to_viewpoint[clean_word]["Value"]))):
                continue

            if(first_word):
               word = word.capitalize()
               first_word = False

            last_symbol = word[len(word) - 1]
            if(last_symbol in DELIMETERS_SENTENCE_END):
               first_word = True

            new_words.append(word)

        sentence = " ".join(new_words)
        sentence_len = len(sentence)

        if(sentence_len <= 0):
            return False

        targets_object = self.get_targets(predetermined_targets)
        targets_amount = targets_object["targets_amount"]
        targets = targets_object["targets"]

        targets_text = self.get_targets_text(targets_amount, targets)

        last_symbol = sentence[sentence_len - 1]
        if(last_symbol not in DELIMETERS_SENTENCE_END):
            if(last_symbol in DELIMETERS):
                sentence = sentence[:-1]
                sentence += random.choice(DELIMETERS_SENTENCE_END)
            else:
                sentence += random.choice(DELIMETERS_SENTENCE_END)

        if(verb is None):
            verb = LOCALE[LOCALE_LANGUAGE]["Quotes"] + " <span class='speech_name'>" + speaker.name + "</span>"

        print_sentence = sentence
        sentence = targets_text + sentence
        if(print_say_target):
            print_sentence = targets_text + print_sentence

        my_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
        my_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

        to_chat("<span class='speech_name'>" + self.name + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>(</span>" +
                "<span style='color: " + my_ideology_fg + "'>" + LOCALE[LOCALE_LANGUAGE][self.ideology_name] + "</span>" +
                "<span style='color: " + my_ideology_bg + "'>)</span>" +
                "<span class='speech_verb'> " + verb + ", </span>" +
                "<span class='speech_wrapper'><span style='color: " + bg_color + "'>\"</span></span>" +
                "<span style='color: " + fg_color + "'>" + print_sentence + "</span>" +
                "<span class='speech_wrapper'><span style='color: " + bg_color + "'>\"</span></span>")

        to_hear = global_vars.citizens.copy()
        to_hear.remove(self)
        random.shuffle(to_hear)

        for citizen in to_hear:
            citizen.queue_hear(self, verb, sentence, predetermined_triggers, proxy_speaker=speaker)

        return True

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
        offend_chance = abs(self.political_view.viewpoints[viewpoint_name].value - target.political_view.viewpoints[viewpoint_name].value) * 0.25 * (1.0 - self.tolerancy)
        # The other 50 comes from how much we hate the person.
        offend_chance += (-self.relationships[target.name].title_reaction_mod) * 0.5  # title_reaction_mod is dependant on relationship title, and not the value itself.
        return prob(offend_chance)

    def crit_persuaded_prob(self, speaker, viewpoint_name, favour):
        # The little + 1 at the end ensures that even the stubbornesst of listeners one day may be persuaded...
        return prob((1.0 - self.get_stubborness(viewpoint_name)) * speaker.get_persuasiveness(viewpoint_name) * favour * 100 + 1)

    def listen_to_speaker_check(self, speaker, word, verb, sentence):
        intonation_delimeter = sentence[len(sentence) - 1]
        favour = self.favour_intonations[intonation_delimeter]

        if(word):
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

    def update_relationship_title(self, target_name):
        for relation_type in RELATIONSHIP_THRESHOLDS:
            if(self.relationships[target_name].value >= relation_type["Min"] and
               self.relationships[target_name].value <= relation_type["Max"]):
                if(self.relationships[target_name].title == relation_type["Name"]):
                    return False
                self.relationships[target_name].title = relation_type["Name"]
                self.relationships[target_name].title_color = relation_type["Color"]
                self.relationships[target_name].title_reaction_mod = relation_type["Reaction_Mod"]
                return True

        if(self.relationships[target_name].title == "None"):
            return False

        self.relationships[target_name].title = "None"
        self.relationships[target_name].title_color = 'white'
        self.relationships[target_name].title_reaction_mod = 0
        return True

    def adjust_relationship_value(self, target, value):
        """
        Adjusts our relationship towards target by value.
        Returns by how much we actually changed the relationship towards them.
        """
        return self.relationships[target.name].adjust_value(self, target, value)

    def shift_relationships_and_print(self, args):
        speaker = args[0]
        value = args[1]

        shift_value = self.adjust_relationship_value(speaker, value)
        to_chat_relationship_shift(self, speaker, shift_value)

        old_relationship_title = LOCALE[LOCALE_LANGUAGE][self.relationships[speaker.name].title]
        old_relationship_title_color = self.relationships[speaker.name].title_color

        if(self.update_relationship_title(speaker.name)):  # If it actually did change.
            new_relationship_title = LOCALE[LOCALE_LANGUAGE][self.relationships[speaker.name].title]
            new_relationship_title_color = self.relationships[speaker.name].title_color

            if(print_relationship_changes):
                to_chat("<span class='emote_name'>" + self.name + "</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Relationship Changed To"] + " </span>" +
                        "<span class='emote_name'>" + speaker.name + "</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["From"] + " </span>" +
                        "<span style='color: " + old_relationship_title_color + "'>" + old_relationship_title + "</span>" +
                        "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["To"] + " </span>" +
                        "<span style='color: " + new_relationship_title_color + "'>" + new_relationship_title + "</span>" +
                        "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")

    def non_motivated_action(self):
        """
        What we do, when we're not reacting to anything.
        """
        my_ideology_fg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Foreground"]
        my_ideology_bg = IDEOLOGIES_CLASSIFICATION[self.ideology_name]["Background"]

        triggers = MESSAGE_TRIGGER_NONE

        check_triggers = MESSAGE_TRIGGER_POSSIBILITIES.copy()
        random.shuffle(check_triggers)
        for trigger in check_triggers:
            if(prob(self.emotions.emotionality * 100)):
                triggers = triggers | trigger

        if(not self.say(predetermined_targets=None, predetermined_triggers=triggers, fg_color=my_ideology_fg, bg_color=my_ideology_bg)):  # Political broadcasts don't have predetermined targets.
            if(len(self.to_quote) > 0):
                to_quote_obj = random.choice(to_quote)
                to_quote.remove(to_quote_obj)

                speaker = to_quote_obj["speaker"]
                sentence = to_quote_obj["text"]

                self.quote(speaker, sentence, predetermined_targets=None, predetermined_triggers=triggers|MESSAGE_TRIGGER_QUOTE, fg_color=my_ideology_fg, bg_color=my_ideology_bg)
                return

            # We are seemingly silent, but seem to have a book in our inventory. Why not read it/give it out?
            for book in self.inventory:
                if(book.can_use(self, self)):  # Can we read it?
                    book.use(self, self)
                else:
                    give_to = random.choice(global_vars.citizens)
                    if(give_to != self):
                        book.give(self, give_to)

            # We are seemingly silent, what about trying to write up a book?
            total_stubborness = 0.0
            viewpoint_names = self.political_view.viewpoints.keys()
            viewpoints_amount = len(viewpoint_names)

            for viewpoint_name in viewpoint_names:
                total_stubborness += self.get_stubborness(viewpoint_name)

            if(prob((1.0 - self.vocal) * (total_stubborness / viewpoints_amount) * 100)):  # We are both stubborn enough, and silent enough to write a book.
                self.write_book(total_stubborness / viewpoints_amount)

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["age"] = self.age
        saveObject["name"] = self.name

        saveObject["vocal"] = self.vocal
        saveObject["tolerancy"] = self.tolerancy

        saveObject["political_view"] = self.political_view.get_save_state()
        saveObject["emotions"] = self.emotions.get_save_state()

        # There is no point in saving the ideology, since values for it could be changed.
        # saveObject["ideology_name"] = self.ideology_name

        saveObject["favour_words"] = self.favour_words.copy()
        saveObject["dislike_words"] = self.dislike_words.copy()

        saveObject["favour_intonations"] = self.favour_intonations.copy()
        saveObject["dislike_intonations"] = self.dislike_intonations.copy()

        saveObject["favour_word_uppercase"] = self.favour_word_uppercase.copy()
        saveObject["dislike_word_uppercase"] = self.dislike_word_uppercase.copy()

        # saveObject["to_quote"] = self.to_quote.copy()

        saveObject["relationships"] = {}
        for citizen_name in self.relationships.keys():
            saveObject["relationships"][citizen_name] = self.relationships[citizen_name].get_save_state()

        saveObject["inventory"] = []
        for item in self.inventory:
            if(isinstance(item, Book)):  # They use a different system, due to weak-name-links.
                continue
            saveObject["inventory"].append(item.get_save_state())

        return saveObject

    def load_save_state(saveObject):
        me = str_to_class(saveObject["type"])(None, saveObject)
        return me


class Player(Citizen):
    def get_sentence(self, targets, targets_text, words_amount, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan'):
        to_print_targets = targets_text
        if(len(to_print_targets) > 2):
            to_print_targets = to_print_targets[:-2]

        to_chat("<span class='warn_player'>Player's turn, awaiting your message! Targets will be: " + to_print_targets + "</span>")
        global_vars.awaiting_npc_message = True
        global_vars.last_npc_message = None
        if(global_vars.player_count > 0):
            timeout_time = 15
            for i in range(timeout_time):
                if(not global_vars.awaiting_npc_message):
                    break
                time.sleep(1)

        if(global_vars.last_npc_message is None):
            to_chat("<span class='warn_player'>Timeout, your messages will no longer be considered!</span>")
            return super().get_sentence(targets, targets_text, words_amount, predetermined_triggers, fg_color, bg_color)
        else:
            sentence = str(global_vars.last_npc_message)
            sentence_len = len(sentence)
            last_symbol = sentence[sentence_len - 1]
            if(last_symbol not in DELIMETERS_SENTENCE_END):
                if(last_symbol in DELIMETERS):
                    sentence = sentence[:-1]
                    sentence += random.choice(DELIMETERS_SENTENCE_END)
                else:
                    sentence += random.choice(DELIMETERS_SENTENCE_END)
            return sentence


class View:
    def __init__(self, saveObject={}):
        self.viewpoints = {}
        pos_viewpoints = get_all_subclasses(Viewpoint)

        for viewpoint in pos_viewpoints:
            if("viewpoints" in saveObject.keys() and viewpoint.name in saveObject["viewpoints"].keys()):
                view_type = str_to_class(saveObject["viewpoints"][viewpoint.name]["type"])
                view = view_type.load_save_state(saveObject["viewpoints"][viewpoint.name])
            else:
                view = viewpoint()

                view.value = random.randrange(-100, 101)
                view.stubborness = random.uniform(0.0, 1.0)
                view.persuasiveness = random.uniform(0.0, 1.0)

            self.viewpoints[view.name] = view

    def generate_political_axis(self):
        axis = {}
        for viewpoint_name in self.viewpoints:
            axis[viewpoint_name] = self.viewpoints[viewpoint_name].value
        return axis

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
        saveObject["type"] = self.__class__.__name__

        saveObject["viewpoints"] = {}
        for viewpoint_name in self.viewpoints.keys():
            saveObject["viewpoints"][viewpoint_name] = self.viewpoints[viewpoint_name].get_save_state()

        return saveObject

    def load_save_state(saveObject):
        me = str_to_class(saveObject["type"])(saveObject)
        return me


class Faction:
    def __init_(self, leader):
        self.leader = leader
        self.members = [leader]

        self.political_view = leader.political_view

"""
rel_cache = {}
"""

class Relationship:
    def __init__(self):
        self.value = 0  # We don't know anybody yet.

        self.permanent_min_val_modifier = 0  # Tweak this to allow this relationship to ever be worse.
        self.permanent_max_val_modifier = 0  # Tweak this to allow this relationship to be even better.

        self.title = "None"  # Respect, like, dislike, hate.
        self.title_color = 'w'
        self.title_reaction_mod = 0

    def adjust_value(self, us, target, value):
        """
        Adjusts self.value by value.
        Returns by how much we actually adjusted.
        """
        if(value < 0.1 and value > -0.1):
            return 0.0

        min_pos = self.get_min_possible(us, target)
        max_pos = self.get_max_possible(us, target)

        """
        cache_string = us.name + "\\" + target.name
        times_changed = 0
        if(cache_string in rel_cache):
            if(rel_cache[cache_string]["times_changed"] > 1):
                to_chat(("Us:", us.name, "Them:", target.name, "Times_changed:", rel_cache[cache_string]["times_changed"]))
                to_chat(("Cur:", self.value, "Prev:", rel_cache[cache_string]["prev"], "To_change:", value))
                to_chat(("Min:", min_pos, "Prev_min:", rel_cache[cache_string]["prev_min"]))
                to_chat(("Max:", max_pos, "Prev_max:", rel_cache[cache_string]["prev_max"]))
            times_changed = rel_cache[cache_string]["times_changed"] + 1
        rel_cache[cache_string] = {"prev": self.value, "prev_max": max_pos, "prev_min": min_pos, "times_changed": times_changed}
        """

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
        axis_count = len(IDEOLOGIES_CLASSIFICATION[us.ideology_name]["Axis"])
        max_distance_per_axis = 200 ** 2

        max_possible_distance = axis_count * max_distance_per_axis

        for axis in IDEOLOGIES_CLASSIFICATION[us.ideology_name]["Axis"]:
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
            axis_count = len(IDEOLOGIES_CLASSIFICATION[us.ideology_name]["Axis"])
            max_distance_per_axis = 200 ** 2

            max_possible_distance = axis_count * max_distance_per_axis

            for axis in IDEOLOGIES_CLASSIFICATION[us.ideology_name]["Axis"]:
                ideological_distance += (us.political_view.viewpoints[axis].value - target.political_view.viewpoints[axis].value) ** 2

            love_from_ideology = translate(round(math.sqrt(ideological_distance), 1), 0, round(math.sqrt(max_possible_distance), 1), 50, 0)

            retVal += love_from_ideology

        retVal = round(retVal, 1)

        return clamp(retVal, -100.0, 100.0)

    def get_reaction_modifier(self, us, speaker):
        return self.title_reaction_mod

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["value"] = self.value
        saveObject["permanent_min_val_modifier"] = self.permanent_min_val_modifier
        saveObject["permanent_max_val_modifier"] = self.permanent_max_val_modifier

        """
        self.title, self.title_color, self.title_reaction_mod could be changed if we change some default values, there is no point
        in saving them.
        """

        return saveObject

    def load_save_state(saveObject):
        me = str_to_class(saveObject["type"])()

        me.value = saveObject["value"]
        me.permanent_min_val_modifier = saveObject["permanent_min_val_modifier"]
        me.permanent_max_val_modifier = saveObject["permanent_max_val_modifier"]

        return me


class Emotions:
    def __init__(self, saveObject={}):
        if("emotionality" in saveObject.keys()):
            self.emotionality = saveObject["emotionality"]
        else:
            self.emotionality = random.uniform(0.0, 1.0)

        self.reactions_speaker = {}
        self.reactions_provoker = {}

        for possible_trigger in MESSAGE_TRIGGER_POSSIBILITIES:
            self.reactions_speaker[str(possible_trigger)] = generate_reaction(self.emotionality, possible_trigger, saveObject)
            self.reactions_provoker[str(possible_trigger)] = generate_reaction(self.emotionality, possible_trigger, saveObject)

    def react_to_triggers(self, us, speaker, provoker, triggers, text=""):
        """
        Return True to interupt default reaction - speech.

        us - is the Citizen reacting.
        speaker - is the Citizen, that emitted the emotion.
        provoker - is the Citizen who provoked the emotion in speaker.
        """
        retVal = False

        check_triggers = MESSAGE_TRIGGER_POSSIBILITIES.copy()
        random.shuffle(check_triggers)

        for possible_trigger in check_triggers:
            if(triggers & possible_trigger):
                if(self.reactions_speaker[str(possible_trigger)].react_check(us, speaker)):
                    retVal = self.reactions_speaker[str(possible_trigger)].invoke(us, speaker, text=text) or retVal
                # Do not react to those who provoked, if they are ourselves... TODO: Add insanity.
                if(provoker is not None and provoker is not us and self.reactions_provoker[str(possible_trigger)].react_check(us, provoker)):
                    retVal = self.reactions_provoker[str(possible_trigger)].invoke(us, provoker, text=text) or retVal
        return retVal

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["emotionality"] = self.emotionality

        saveObject["reactions_speaker"] = {}
        for reaction_trigger in self.reactions_speaker.keys():
            saveObject["reactions_speaker"][reaction_trigger] = self.reactions_speaker[reaction_trigger].get_save_state()
        saveObject["reactions_provoker"] = {}
        for reaction_trigger in self.reactions_provoker.keys():
            saveObject["reactions_provoker"][reaction_trigger] = self.reactions_provoker[reaction_trigger].get_save_state()

        return saveObject

    def load_save_state(saveObject):
        me = str_to_class(saveObject["type"])(saveObject)

        return me


class Item:
    name = "Item"

    def give(self, user, target):
        user.inventory.remove(self)
        target.inventory.append(self)
        to_chat("<span class='emote_name'>" + user.name + "</span>" +
                "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Gives"] + " </span>" +
                "<span class='emote_name'>" + target.name + " </span>" +
                self.name +
                "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")

    def pickup(self, user):
        user.inventory.append(self)

    def can_use(self, user, target):
        return False

    def use(self, user, target):
        return

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["name"] = self.name

        return saveObject

    def load_save_state(saveObject):
        me = str_to_class(saveObject["type"])()

        me.name = saveObject["name"]
        return me

class Book(Item):
    name = "Book"

    def __init__(self, creator, created_name, text):
        super().__init__()
        self.name = created_name
        self.created_by = creator
        self.text = text
        self.ideology = creator.ideology_name

        self.read_by_names = [creator.name]  # We can't convince us with our own book.

        global_vars.all_books.append(self)

    def can_use(self, user, target):
        return target.name not in self.read_by_names

    def use(self, user, target):
        self.read_by_names.append(target.name)

        all_read = True
        for citizen in global_vars.citizens:
            if(citizen not in self.read_by_names):
                all_read = False
                break

        if(all_read):
            all_books.remove(self)
            user.inventory.remove(self)

        target.hear(self.created_by, "writes", self.text, MESSAGE_TRIGGER_NONE)
        to_chat("<span class='emote_name'>" + target.name + "</span>" +
                "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Reads"] + " </span>" +
                self.name +
                "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")

    def get_save_state(self):
        saveObject = super().get_save_state()

        saveObject["created_by_name"] = self.created_by.name
        saveObject["text"] = self.text

        return saveObject

    def load_save_state(saveObject):
        creator = None

        for citizen in global_vars.citizens:
            if(citizen.name == saveObject["created_by_name"]):
                creator = citizen
                break

        if(creator is not None):
            me = str_to_class(saveObject["type"])(creator, saveObject["name"], saveObject["text"])
            return me

        return None


def save_server_state():
    save_state("last")
    save_state()


if(__name__ == "__main__"):
    init_reference_lists()
    init_citizens()

    import server

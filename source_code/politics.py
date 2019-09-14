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

import config_loader
from config_loader import CONFIG_VALUES as CFG

from defines import *

from locale_game import LOCALE
from ideologies_game import IDEOLOGIES_CLASSIFICATION

from collections import deque

"""
Setting up CONFIG.
"""
CONFIG_REQUEST = {
    "DEBUG": {"cfg_type": "bool", "def_value": False},  # config_loader only outputs messages if this is True.

    "SECRET_KEY": {"cfg_type": "key"},  # This is not in the config.cfg, as it is always generated completely at random.
    "PORT": {"cfg_type": "int", "def_value": 8080, "min_val": 0, "max_val": 65535},
    "UPDATE_CACHE": {"cfg_type": "bool", "def_value": False},
    "MAX_PLAYER_COUNT": {"cfg_type": "int", "def_value": 30, "min_val": 0, "max_val": 100},

    "LOCALE_LANGUAGE": {"cfg_type": "str", "def_value": "en", "min_val": 0, "max_val": 2, "possible_values": ["en", "ru", "la"]},

    "MAX_WORDS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},
    "MAX_TARGETS": {"cfg_type": "int", "def_value": 10, "min_val": 1, "max_val": 30},
    "ALL_TARGETS_THRESHOLD": {"cfg_type": "int", "def_value": 5, "min_val": 1, "max_val": 30},
    "MAX_BOOK_SENTENCES": {"cfg_type": "int", "def_value": 20, "min_val": 1, "max_val": 30},

    "DEFAULT_RELATIONSHIP_SHIFT_VALUE": {"cfg_type": "float", "def_value": 2.0, "min_val": 0.0, "max_val": 100.0},
    "INITIAL_RELATIONSHIP_VALUE": {"cfg_type": "float", "def_value": 1.0, "min_val": -100.0, "max_val": 100.0, "prohibited_values": [0.0]},

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
    "ALL_TARGETS_THRESHOLD": {"cfg_type": "int", "def_value": 2019, "min_val": 0, "max_val": 4000},

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

viewpoints_by_word = {}
offensive_to_viewpoint = {}

locale_to_original = {}
original_to_locale = {}

taken_clean_citizen_names = []  # Clean currently means lowercase.

actions_queue = deque([])  # So we won't be in a mess.
reactions_queue = deque([])

RELATIONSHIP_THRESHOLDS = [
    {"Name": "Reverence", "Min": 90, "Max": 100, "Color": 'green; font-weight: bold', "Reaction_Mod": 90},
    {"Name": "Respect", "Min": 50, "Max": 90, "Color": 'green', "Reaction_Mod": 50},
    {"Name": "Sympathy", "Min": 25, "Max": 50, "Color": 'white', "Reaction_Mod": 25},
    {"Name": "Distaste", "Min": -50, "Max": -25, "Color": 'white', "Reaction_Mod": -25},
    {"Name": "Hate", "Min": -90, "Max": -50, "Color": 'red', "Reaction_Mod": -50},
    {"Name": "Feud", "Min": -100, "Max": -90, "Color": 'red; font-weight: bold', "Reaction_Mod": -90}
]

all_books = []

# These are required for player to NPC interaction.
clients_by_sid = {}
client_infos_by_ip = {}

max_player_count = CFG["MAX_PLAYER_COUNT"]
player_count = 0
await_npc_message = False
last_npc_message = None

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

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

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


def generate_reaction(emotionality, possible_trigger, speaker=True, load_from=dict()):
    """
    speaker - is how we react to somebody expressing emotion.
    speaker false - is how we react to somebody who provoked an emotion in somebody else.
    """
    reaction_class = None
    trigger_hapiness = 0
    if("Reactions" in load_from and type(load_from["Reactions"]) is dict and str(possible_trigger) in load_from["Reactions"].keys()):
        target_type = "Speaker"
        if(not speaker):
            target_type = "Provoker"

        if(target_type in load_from["Reactions"][str(possible_trigger)].keys()):
            reaction_handler = load_from["Reactions"][str(possible_trigger)][target_type]
            reaction_class = str_to_class(reaction_handler["Type"])
            if("Trig" in reaction_handler.keys()):
                trigger_hapiness = reaction_handler["Trig"]

    if(reaction_class is None):
        trigger_hapiness = random.uniform(-1.0, 1.0)
        reaction_class = random.choice(get_all_subclasses(Reaction))
    return reaction_class(emotionality, trigger_hapiness)


def to_chat(text):
    for client_info in client_infos_by_ip.values():
        if(client_info.loaded):
            client_info.saved_messages.append(text)

    speak_to = list(clients_by_sid.values()).copy()
    for client in speak_to:
        if(not client.disconnecting):
            client.whisper(text)
    # socketio.emit('npc_message', {"data": text})

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
        self.emotions = Emotions(views_preset)

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

        self.to_quote = []  # Things this very citizen would like to quote in the future, whenever they can.

        self.relationships = {}
        for citizen in citizens:
            self.relationships[citizen.name] = Relationship()
            self.adjust_relationship_value(citizen, CFG["INITIAL_RELATIONSHIP_VALUE"])
            citizen.relationships[self.name] = Relationship()
            citizen.adjust_relationship_value(self, CFG["INITIAL_RELATIONSHIP_VALUE"])

        self.inventory = []

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
            self.dislike_intonations[intonation] = random.uniform(0.0, CFG["DISLIKE_DELIMITERS_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

    def generate_uppercase_relation(self):
        for word_uppercase in WORD_UPPERCASE_POSSIBILITIES:
            self.favour_word_uppercase[word_uppercase] = random.uniform(0.0, 1.0)  # How much we like when the word is shouted, or said with uppercase. Where 0 is we don't like it at all, 1 is we like the word very much.
            self.dislike_word_uppercase[word_uppercase] = random.uniform(0.0, CFG["DISLIKE_UPPERCASE_MAXIMUM"])  # It may be convincing, but we may dislike it on emotional level.

    def get_targets(self, predetermined_targets=None):
        targets_amount = 0
        targets = []
        if(type(predetermined_targets) is not list):
            targets_amount = round(CFG["MAX_TARGETS"] * random.uniform(0.0, self.vocal))
            if(targets_amount == 0):
                return {"targets_amount": targets_amount, "targets": targets}

            for t in range(targets_amount):
                new_target = random.choice(citizens)
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

    def queue_say(self, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan'):
        global actions_queue

        actions_queue.append(
            {
                "speaker": self,
                "type": "say",
                "predetermined_targets": predetermined_targets,
                "predetermined_triggers": predetermined_triggers,
                "fg_color": fg_color,
                "bg_color": bg_color
            })

    def say(self, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan'):
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
        verb = self.get_verb(sentence)

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

        to_hear = citizens.copy()
        to_hear.remove(self)
        random.shuffle(to_hear)

        for citizen in to_hear:
            citizen.queue_hear(self, verb, sentence, predetermined_triggers)

        return True

    def queue_hear(self, speaker, verb, sentence, predetermined_triggers, proxy_speaker=None, on_hear_done=None, on_hear_done_args=None):
        global reactions_queue

        reactions_queue.appendleft(
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
            to_see_persuade = citizens.copy()
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

        to_chat_relationship_shift(self, speaker, self.adjust_relationship_value(speaker, relationship_shift))
        if(proxy_speaker and proxy_speaker != self and proxy_speaker != speaker):
            to_chat_relationship_shift(self, proxy_speaker, self.adjust_relationship_value(proxy_speaker, relationship_shift))

        old_relationship_title = LOCALE[LOCALE_LANGUAGE][self.relationships[speaker.name].title]
        old_relationship_title_color = self.relationships[speaker.name].title_color

        if(self.update_relationship_title(speaker)):  # If it actually did change.
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
        if(clean_word in viewpoints_by_word.keys()):
            viewpoint_name = viewpoints_by_word[clean_word]["Viewpoint"]

            base_value *= (1.0 - self.get_stubborness(viewpoint_name)) * speaker.get_persuasiveness(viewpoint_name)

            favour *= (self.relationships[speaker.name].value + 100) / 200  # If we dislike them as a person they have a lower chance to persuade us.

            if(self.crit_persuaded_prob(speaker, viewpoint_name, favour)):
                dislike *= CFG["CRIT_PERSUASION_DISLIKE_MULTIPLIER"]  # We were very much persuaded. We do not hate this person at all.

                self.relationships[speaker.name].permanent_min_val_modifier += CFG["RELATIONSHIP_PERM_MODIFIER_ON_CRIT_PERSUASION"]
                self.relationships[speaker.name].permanent_max_val_modifier += CFG["RELATIONSHIP_PERM_MODIFIER_ON_CRIT_PERSUASION"]

                base_value *= CFG["CRIT_PERSUASION_MULTIPLIER"]

                # If our viewpoint is of same value as of person's who persuaded us, we gain a convincing argument which strengthens our stubborness.
                # Otherwise, we become somewhat less stubborn.
                if(sign(self.political_view.viewpoints[viewpoint_name].value) == sign(viewpoints_by_word[clean_word]["Value"])):
                   self.political_view.viewpoints[viewpoint_name].stubborness += CFG["CRIT_PERSUASION_STUBBORNESS_MODIFIER"]
                else:
                   self.political_view.viewpoints[viewpoint_name].stubborness -= CFG["CRIT_PERSUASION_STUBBORNESS_MODIFIER"]

                message_triggers = message_triggers | MESSAGE_TRIGGER_PERSUASIVE

        base_value *= (1.0 - dislike)

        relationship_value *= favour - dislike

        return {"Viewpoint": viewpoint_name, "Viewpoint_Shift_Value": base_value, "Relationship_Shift_Value": relationship_value, "Message_Triggers": message_triggers}

    def queue_emote(self, emotion, emotion_target=None, predetermined_targets=None, predetermined_triggers=MESSAGE_TRIGGER_NONE, on_emote_done=None, on_emote_done_args=None):
        global actions_queue

        actions_queue.append(
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
                new_target = random.choice(citizens)
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
            emotion_target_text = " " + "<span class='speech_name'>" + emotion_target.name + "</span>"

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
        global reactions_queue

        reactions_queue.appendleft(
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

    # book, predetermined_triggers=MESSAGE_TRIGGER_NONE
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

            to_hear = citizens.copy()
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
            if(clean_word in taken_clean_citizen_names):
                continue
            if(clean_word == LOCALE[LOCALE_LANGUAGE]["All"].lower()):
                continue

            if(clean_word in viewpoints_by_word.keys() and (sign(self.political_view.viewpoints[viewpoints_by_word[clean_word]["Viewpoint"]].value) != sign(viewpoints_by_word[clean_word]["Value"]))):
                continue

            if(clean_word in offensive_to_viewpoint.keys() and (sign(self.political_view.viewpoints[offensive_to_viewpoint[clean_word]["Viewpoint"]].value) == sign(offensive_to_viewpoint[clean_word]["Value"]))):
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

        to_hear = citizens.copy()
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

    def update_relationship_title(self, target):
        for relation_type in RELATIONSHIP_THRESHOLDS:
            if(self.relationships[target.name].value >= relation_type["Min"] and
               self.relationships[target.name].value <= relation_type["Max"]):
                if(self.relationships[target.name].title == relation_type["Name"]):
                    return False
                self.relationships[target.name].title = relation_type["Name"]
                self.relationships[target.name].title_color = relation_type["Color"]
                self.relationships[target.name].title_reaction_mod = relation_type["Reaction_Mod"]
                return True

        if(self.relationships[target.name].title == "None"):
            return False

        self.relationships[target.name].title = "None"
        self.relationships[target.name].title_color = 'white'
        self.relationships[target.name].title_reaction_mod = 0
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
                    give_to = random.choice(citizens)
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


class Player(Citizen):
    def get_sentence(self, targets, targets_text, words_amount, predetermined_triggers=MESSAGE_TRIGGER_NONE, fg_color='white', bg_color='cyan'):
        global awaiting_npc_message
        global last_npc_message

        to_print_targets = targets_text
        if(len(to_print_targets) > 2):
            to_print_targets = to_print_targets[:-2]

        to_chat("<span class='warn_player'>Player's turn, awaiting your message! Targets will be: " + to_print_targets + "</span>")
        awaiting_npc_message = True
        last_npc_message = None
        if(player_count > 0):
            timeout_time = 15
            for i in range(timeout_time):
                if(not awaiting_npc_message):
                    break
                time.sleep(1)

        if(last_npc_message is None):
            to_chat("<span class='warn_player'>Timeout, your messages will no longer be considered!</span>")
            return super().get_sentence(targets, targets_text, words_amount, predetermined_triggers, fg_color, bg_color)
        else:
            sentence = str(last_npc_message)
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
    def __init__(self, views_preset):
        self.viewpoints = dict()
        pos_viewpoints = get_all_subclasses(Viewpoint)

        for viewpoint in pos_viewpoints:
            view = viewpoint()

            self.viewpoints[view.name] = view
            if("Axis" in views_preset and view.name in views_preset["Axis"]):
                view.value = views_preset["Axis"][view.name]["Value"]
                view.stubborness = views_preset["Axis"][view.name]["Stubborness"]
                view.persuasiveness = views_preset["Axis"][view.name]["Persuasiveness"]
            else:
                view.stubborness = random.uniform(0.0, 1.0)
                view.persuasiveness = random.uniform(0.0, 1.0)

    def generate_political_axis(self):
        axis = {}
        for viewpoint_name in self.viewpoints:
            axis[viewpoint_name] = self.viewpoints[viewpoint_name].value
        return axis

    def get_sentence(self, pos_viewpoints, viewpoints_points, viewpoints_offense_points, citizen_vocality, targets_text):
        global print_say_target

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
        # self.value = random.randrange(-100, 101)  # From 100(Left part of name) to -100(Right)
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


class Emotions:
    def __init__(self, load_from=dict()):
        if("Emotionality" in load_from):
            self.emotionality = load_from["Emotionality"]
        else:
            self.emotionality = random.uniform(0.0, 1.0)

        self.reactions_speaker = {}
        self.reactions_provoker = {}
        self.trigger_severity = {}

        for possible_trigger in MESSAGE_TRIGGER_POSSIBILITIES:
            self.reactions_speaker[str(possible_trigger)] = generate_reaction(self.emotionality, possible_trigger, load_from)
            self.reactions_provoker[str(possible_trigger)] = generate_reaction(self.emotionality, possible_trigger, load_from)
            self.trigger_severity[str(possible_trigger)] = random.uniform(-1.0, 1.0)

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


class Reaction:
    incompatibile_tags = []

    def __init__(self, emotionality, trigger_hapiness):
        self.emotionality = emotionality
        self.trigger_hapiness = trigger_hapiness

    def react_check(self, us, speaker):
        # The min 99 is required as to prevent infinite reaction loops...
        return prob(min((self.emotionality * self.trigger_hapiness) * 100 + us.relationships[speaker.name].get_reaction_modifier(us, speaker), 99))

    def invoke(self, us, speaker, text=""):
        """
        us - is the Citizen reacting.
        speaker - is the Citizen, that emitted the emotion, or the citizen who provoked some other Citizen to react in one way or the other.
        """
        return self.on_invoke(us, speaker, text=text)

    def on_invoke(self, us, speaker, text):
        """
        Return True to interupt default reaction - speech.
        """
        return False


class Absent(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        return False


class Ignore(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        return True  # Absent is no reaction, ignore is not even talk back.


class Offensive(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_say(predetermined_targets=[speaker], predetermined_triggers=MESSAGE_TRIGGER_OFFENSIVE)
        return True  # We already said something. Mostly, an offensive word.


class Defensive(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("cry", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_DEFENSIVE)
        return False


class Parent(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("lecture", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_PARENT)
        return False


class Awe(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("awe", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_AWE,
                       on_emote_done=us.shift_relationships_and_print, on_emote_done_args=[speaker, CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"] * self.emotionality])
        return False


class Praise(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("praise", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_PRAISE,
                       on_emote_done=us.shift_relationships_and_print, on_emote_done_args=[speaker, CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"] * self.emotionality])
        us.queue_say(predetermined_targets=[speaker], predetermined_triggers=MESSAGE_TRIGGER_PRAISE)
        return True


class Dissapointment(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("dissapointment", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_DISSAPOINTMENT,
                       on_emote_done=us.shift_relationships_and_print, on_emote_done_args=[speaker, -CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"] * self.emotionality])
        return False


class Curse(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        us.queue_emote("curse", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_CURSE,
                       on_emote_done=us.shift_relationships_and_print, on_emote_done_args=[speaker, -CFG["DEFAULT_RELATIONSHIP_SHIFT_VALUE"] * self.emotionality])
        us.queue_say(predetermined_targets=[speaker], predetermined_triggers=MESSAGE_TRIGGER_CURSE)
        return True


class Write(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        total_stubborness = 0.0
        viewpoint_names = us.political_view.viewpoints.keys()
        viewpoints_amount = len(viewpoint_names)

        for viewpoint_name in viewpoint_names:
            total_stubborness += us.get_stubborness(viewpoint_name)

        book = us.write_book(total_stubborness / viewpoints_amount, [speaker])
        if(book):
            return True
        return False


class Criticize(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        total_stubborness = 0.0
        viewpoint_names = us.political_view.viewpoints.keys()
        viewpoints_amount = len(viewpoint_names)

        for viewpoint_name in viewpoint_names:
            total_stubborness += us.get_stubborness(viewpoint_name)

        book = us.write_book(total_stubborness / viewpoints_amount, [speaker])
        if(book):
            book.give(us, speaker)
            return True
        return False


class Preach(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        for book in us.inventory:
            if(book.ideology == us.ideology_name):
                us.queue_emote("preach", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_PARENT,
                               on_emote_done=us.read_book,
                               on_emote_done_args={"book": book, "predetermined_triggers": MESSAGE_TRIGGER_PARENT, "quote": False})
                return True
        return False


class Misread_Preach(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        for book in us.inventory:
                us.queue_emote("preach", emotion_target=speaker, predetermined_triggers=MESSAGE_TRIGGER_PARENT,
                               on_emote_done=us.read_book,
                               on_emote_done_args={"book": book, "predetermined_triggers": MESSAGE_TRIGGER_QUOTE|MESSAGE_TRIGGER_PARENT, "quote": True})
                return True
        return False


class Quote_Remember(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        if(len(text) > 0):
            us.to_quote.append({"speaker": speaker, "text": text})
        return False


class Quote_Reply(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        if(len(us.to_quote) > 0):
            to_quote_obj = random.choice(us.to_quote)
            us.to_quote.remove(to_quote_obj)

            quotee = to_quote_obj["speaker"]
            sentence = to_quote_obj["text"]

            us.quote(quotee, sentence, predetermined_targets=[speaker], predetermined_triggers=MESSAGE_TRIGGER_QUOTE)
            return True
        return False


class Copycat(Reaction):
    incompatible_tags = []

    def on_invoke(self, us, speaker, text):
        if(len(text) > 0):
            us.quote(speaker, text, predetermined_targets=[speaker], predetermined_triggers=MESSAGE_TRIGGER_QUOTE|MESSAGE_TRIGGER_OFFENSIVE)
            return True
        return False


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


class Book(Item):
    name = "Book"

    def __init__(self, creator, created_name, text):
        super().__init__()
        self.name = created_name
        self.created_by = creator
        self.text = text
        self.ideology = creator.ideology_name

        self.read_by_names = [creator.name]  # We can't convince us with our own book.

        all_books.append(self)

    def can_use(self, user, target):
        return target.name not in self.read_by_names

    def use(self, user, target):
        self.read_by_names.append(target.name)

        target.hear(self.created_by, "writes", self.text, MESSAGE_TRIGGER_NONE)
        to_chat("<span class='emote_name'>" + target.name + "</span>" +
                "<span class='emote'> " + LOCALE[LOCALE_LANGUAGE]["Reads"] + "</span>" +
                self.name +
                "<span class='emote'>" + LOCALE[LOCALE_LANGUAGE]["Announcement_end"] + "</span>")


init_reference_lists()

citizens_to_spawn = 25
# citizens_to_spawn = 2
citizens_spawned = 0
citizens = []

from characters_presets import PRESET_CITIZENS

CITIZENS_TO_IMPORT = "All"  # Either "All", "None" or [citizen_name_to_import_1, citizen_name_to_import_2, ...]
# CITIZENS_TO_IMPORT = "None"
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

citizens.append(Player("Player"))

"""
Server part.
"""

can_speak = False

def citizen_speech():
    global can_speak
    while(True):
        if(can_speak):
            break
        time.sleep(1)

    global reactions_queue
    global actions_queue

    while(True):
        if(len(actions_queue) > 0):
            action = actions_queue.popleft()
            if(action["type"] == "say"):
                action["speaker"].say(
                    predetermined_targets=action["predetermined_targets"],
                    predetermined_triggers=action["predetermined_triggers"],
                    fg_color=action["fg_color"],
                    bg_color=action["bg_color"]
                    )
            elif(action["type"] == "emote"):
                action["speaker"].emote(
                    action["emotion"],
                    emotion_target=action["emotion_target"],
                    predetermined_targets=action["predetermined_targets"],
                    predetermined_triggers=action["predetermined_triggers"],
                    on_emote_done=action["on_emote_done"],
                    on_emote_done_args=action["on_emote_done_args"]
                    )
        elif(len(reactions_queue) > 0):
            reaction = reactions_queue.popleft()
            if(reaction["type"] == "hear"):
                reaction["hearer"].hear(
                    reaction["speaker"],
                    reaction["verb"],
                    reaction["sentence"],
                    reaction["predetermined_triggers"],
                    reaction["proxy_speaker"],
                    reaction["on_hear_done"],
                    reaction["on_hear_done_args"]
                    )
            elif(reaction["type"] == "hear_emote"):
                reaction["hearer"].hear_emote(
                    reaction["speaker"],
                    reaction["emotion"],
                    reaction["provoker"],
                    reaction["predetermined_triggers"]
                    )
        else:
            citizen = random.choice(citizens)
            citizen.non_motivated_action()

import threading

from flask import Flask, render_template, send_from_directory, request, escape
from flask_socketio import SocketIO, disconnect


class Client_Info:
    def __init__(self, ip):
        self.username = self.clean_username(random.choice(POS_NAMES) + "_" + random.choice(POS_SURNAMES))

        self.hear_from = []
        for citizen in citizens:
            self.hear_from.append(citizen.name)

        client_infos_by_ip[ip] = self

        self.saved_messages = []

        self.loaded = True

    def clean_username(self, username):
        delimeters_to_remove = "".join(DELIMETERS)
        username_stripped = re.sub("[" + delimeters_to_remove + "]", "", username)
        username_stripped = username_stripped.strip()  # Remove trailing spaces.

        return username


class Client:
    def __init__(self, request):
        global client_infos_by_ip

        self.ip = request.remote_addr
        self.sid = request.sid

        self.can_save = True  # If the player connected from multiple devices, data from some shouldn't be saved as it may get duped.

        if(self.ip in client_infos_by_ip):
            self.client_info = client_infos_by_ip[self.ip]
            self.client_info.loaded = True
        else:
            self.client_info = Client_Info(self.ip)

        self.disconnecting = False

    def on_connect(self):
        global max_player_count
        global player_count
        global clients_by_sid

        player_count += 1
        clients_by_sid[self.sid] = self
        print("Received Connection(" + str(player_count) + "/" + str(max_player_count) + ") from user(" + str(self.ip) + ")")

        for message in self.client_info.saved_messages:
            self.whisper(message, save=False)

        self.whisper("Welcome to Totally Accurate Political Simulator.")

    def on_disconnect(self):
        global max_player_count
        global player_count
        global clients_by_sid

        self.disconnecting = True

        player_count -= 1
        clients_by_sid.pop(self.sid)
        print("Lost Connection(" + str(player_count) + "/" + str(max_player_count) + ") to user(" + str(self.ip) + ")")

        self.client_info.loaded = False

    def whisper(self, message, save=True):
        socketio.emit('npc_message', {"data": message}, room=self.sid)

    def on_npc_message(self, json):
        global awaiting_npc_message
        global last_npc_message

        message = json["data"]
        if(not self.message_check(message)):
            return

        if(awaiting_npc_message):
            last_npc_message = escape(message)
            awaiting_npc_message = False
        # socketio.emit('npc_message', json)

    def on_player_message(self, json):
        message = json["data"]
        if(not self.message_check(message)):
            return

        json = {"data": escape(message)}
        # socketio.emit('player_message', json)

    def message_check(self, message):
        """
        Return True if message passed the check, false otherwise.
        """
        if(message == ""):
            return False

        if(len(message) > 256):
            return False

        return True

    def disconnect(self):
        disconnect(self.sid)


threading.Thread(target=citizen_speech).start()

template_dir = os.path.abspath('../templates')
static_dir = os.path.abspath('../static')

app = Flask(__name__, template_folder=template_dir, static_url_path='')
app.config['SECRET_KEY'] = CFG["SECRET_KEY"]
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

@app.after_request
def after_request(response):
    # Update cache if so required.
    if(CFG["UPDATE_CACHE"]):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(static_dir, path)

@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    global can_speak
    global max_player_count
    global player_count

    if(player_count + 1 > max_player_count):
        print("Disconnected(" + str(player_count) + "/" + str(max_player_count) + ") user(" + str(request.remote_addr) + "). Reason: Server overcrowded")
        disconnect(request.sid)
        return

    can_speak = True

    client = Client(request)
    client.on_connect()

@socketio.on('disconnect')
def on_disconnect(methods=['GET', 'POST']):
    if(request.sid in clients_by_sid.keys()):
        clients_by_sid[request.sid].on_disconnect()

@socketio.on('npc_message')
def on_npc_message(json, methods=['GET', 'POST']):
    if(request.sid in clients_by_sid.keys()):
        clients_by_sid[request.sid].on_npc_message(json)

@socketio.on('player_message')
def on_player_message(json, methods=['GET', 'POST']):
    if(request.sid in clients_by_sid.keys()):
        clients_by_sid[request.sid].on_player_message(json)

socketio.run(app, host='0.0.0.0', port=CFG["PORT"], debug=CFG["DEBUG"])

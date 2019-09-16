"""
THIS MODULE HAS BEEN MADE BY LUDUK AT ningawent@gmail.com
PLEASE CONTACT BEFORE DISTRIBUTING AND OR MODIFYING THIS ON YOUR OWN ACCORD.

I, LUDUK, TAKE NO RESPONSIBILITY FOR ANY MISUES OF THIS MODULE.

also if you don't credit me you're a big meanie
"""

import os
import glob
import json
import random
random = random.SystemRandom()

def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.

    Taken from the django.utils.crypto module.
    """
    return ''.join(random.choice(allowed_chars) for i in range(length))


def get_secret_key():
    """
    Create a random secret key.

    Taken from the Django project.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def str_to_bool(s):
    if(s == 'True'):
         return True
    elif(s == 'False'):
         return False
    else:
         raise ValueError("Cannot covert {} to a bool".format(s)) # evil ValueError that doesn't tell you what the wrong value was


def str_to_list(s):
    retVal = json.loads(s)

    if(retVal is not list):
        raise ValueError("Cannot convert {} to a list".format(s))
        return

    return retVal


def str_to_list_or_str(s):
    retVal = json.loads(s)

    if(retVal is not list):
        return str(s).strp("\"")
    return retVal


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


def find_first_seperator(text, char):
    idx = text.find(char)
    while idx != -1:
        if(idx != 0):
            if(text[idx - 1] != CONFIG_ESCAPE_SYMBOL):
                return idx
        idx = s.find(c, idx + 1)

"""
Before we even try to parse anything we check if we didn't screw up with the code itself.
"""
class Start_Check_Failed(Exception):
    pass


pre_load_messages = []


def before_start_check(CONFIG_REQUEST):
    retVal = type(CONFIG) is dict and type(CONFIG_REQUEST) is dict and len(CONFIG_REQUEST) > 0

    for config in CONFIG_REQUEST.keys():
        if(type(CONFIG_REQUEST[config]) is not dict):
            print_debug("IMPROPER CONFIG PARAM DEFINITION: " + config)
            continue

        if("cfg_type" not in CONFIG_REQUEST[config]):
            print_debug("IMPROPER CONFIG PARAM DEFINITION: " + config)
            continue

        if(CONFIG_REQUEST[config]["cfg_type"] not in CONFIG_ACCEPTED_TYPES):
            print_debug("IMPROPER DEFINED TYPE: " + CONFIG_REQUEST[config]["cfg_type"] + " FOR: " + config)
            continue

        # We init all those given configs that are proper, with at least default values even before reading the file.
        cfg_type = CONFIG_REQUEST[config]["cfg_type"]

        def_value = None
        if("def_value" in CONFIG_REQUEST[config]):
            def_value = CONFIG_REQUEST[config]["def_value"]

        min_val = None
        if("min_val" in CONFIG_REQUEST[config]):
            min_val = CONFIG_REQUEST[config]["min_val"]

        max_val = None
        if("max_val" in CONFIG_REQUEST[config]):
            max_val = CONFIG_REQUEST[config]["max_val"]

        possible_values = None
        if("possible_values" in CONFIG_REQUEST[config] and type(CONFIG_REQUEST[config]["possible_values"]) is list):
            possible_values = CONFIG_REQUEST[config]["possible_values"]

        prohibited_values = None
        if("prohibited_values" in CONFIG_REQUEST[config] and type(CONFIG_REQUEST[config]["prohibited_values"]) is list):
            prohibited_values = CONFIG_REQUEST[config]["prohibited_values"]

        CONFIG[config] = config_value(config, cfg_type, def_value, min_val, max_val, possible_values, prohibited_values)
        pre_load_messages.append("Set to default: " + config + " " + str(CONFIG[config].value) + " " + str(type(CONFIG[config].value)))

    if(not retVal):
        raise Start_Check_Failed
    return True


"""
Put all possible types of information that can be parsed out of your config here.
"def" is the default value, it will be used if none other is given.
"parse" is the function called to parse our value out of what we pass to it.
"clamp" is the function that clamps between min and max vals for this type.
"def_min" is the default minimum value, it will be used if none other is given.
"def_max" is the default maximum value, it will be used if none other is given.
"""
CONFIG_ACCEPTED_TYPES = {
    "str": {
        "def": "",
        "parse": lambda x : str(x).strip("\""),
        "clamp": lambda x, min_, max_ : x[:-int(len(x) - max_)] if len(x) > max_ else x,
        "def_min": 0,
        "def_max": 1,  # For strings this param stands for length.
        },

    "int": {
        "def": 0,
        "parse": lambda x : int(x),
        "clamp": lambda x, min_, max_ : clamp(x, min_, max_),
        "def_min": 0,
        "def_max": 1,
        },

    "float": {
        "def": 0.0,
        "parse": lambda x : float(x),
        "clamp": lambda x, min_, max_ : clamp(x, min_, max_),
        "def_min": 0.0,
        "def_max": 1.0,
        },

    "bool": {
        "def": False,
        "parse": lambda x : str_to_bool(x),
        "clamp": lambda x, min_, max_ : x,
        "def_min": False,
        "def_max": True,
        },

    "list": {
        "def": [],
        "parse": lambda x : str_to_list(x),
        "clamp": lambda x, min_, max_ : x,
        "def_min": 0,
        "def_max": 0,
        },

    "list_or_str": {
        "def": "",
        "parse": lambda x : str_to_list_or_str(x),
        "clamp": lambda x, min_, max_ : x,
        "def_min": 0,
        "def_max": 0,
        },

    "key": {
        "def": get_secret_key(),
        "parse": lambda x : get_secret_key(),
        "clamp": lambda x, min_, max_ : x[:-int(len(x) - max_)] if len(x) > max_ else x,
        "def_min": 0,
        "def_max": 50,  # 50 random symbols for the key.
    }
}


class config_value:
    def __init__(self, name, config_type, def_value=None, min_val=None, max_val=None, possible_values=None, prohibited_values=None):
        self.name = name
        self.valid = True

        if(config_type in CONFIG_ACCEPTED_TYPES):
            config_type_obj = CONFIG_ACCEPTED_TYPES[config_type]

            self.config_type = config_type
            self.possible_values = possible_values
            self.prohibited_values = prohibited_values

            if min_val is None:
                self.min_val = config_type_obj["def_min"]
            else:
                self.min_val = min_val

            if max_val is None:
                self.max_val = config_type_obj["def_max"]
            else:
                self.max_val = max_val

            if def_value is None:
                self.value = config_type_obj["def"]
            else:
                self.value = def_value
            self.def_value = self.value

            self.overriden = False
        else:
            self.valid = False

        CONFIG_VALUES[self.name] = self.value

    def parse_value_from_string(self, text):
        """
        Return true if value was found in text, false otherwise.
        """
        old_value = self.value

        parsed = CONFIG_ACCEPTED_TYPES[self.config_type]["parse"](text)
        clamped = CONFIG_ACCEPTED_TYPES[self.config_type]["clamp"](parsed, self.min_val, self.max_val)
        self.value = clamped

        if(self.possible_values):
            if(self.value not in self.possible_values):
                print_debug(self.name + " VALUE WAS NOT ALLOWED, RESETTING TO DEFAULT.")
                self.value = self.def_value

        if(self.prohibited_values):
            if(self.value in self.prohibited_values):
                print_debug(self.name + " VALUE WAS PROHIBITED, RESETTING TO DEFAULT.")
                self.value = self.def_value

        if(self.overriden):
            print_debug(self.name + " HAS BEEN OVERRIDEN MULTIPLE TIMES FROM: " + old_value + " TO: " + self.value)

        CONFIG_VALUES[self.name] = self.value
        self.overriden = True


CONFIG_PATH = "../config/"
CONFIG_EXTENSION = ".cfg"
CONFIG_COMMENT_SYMBOL = "#"
CONFIG_SEPERATOR_SYMBOL = "="
CONFIG_ESCAPE_SYMBOL = "\\"

# See config.cfg in CONFIG_PATH for more context and commentary on these.

CONFIG = {}  # This contains config_value objects.
CONFIG_VALUES = {}  # This contants only values of config_value objects.


def print_debug(message):
    if("DEBUG" in CONFIG_VALUES.keys() and CONFIG_VALUES["DEBUG"]):
        print(message)

def main(CONFIG_REQUEST=None):
    try:
        if(before_start_check(CONFIG_REQUEST)):
            CONFIG_KEYS = CONFIG.keys()  # We already initiated CONFIG with config_value objects in before_start_check.

            for filename in glob.glob(CONFIG_PATH + "*" + CONFIG_EXTENSION):
                with open(filename, 'r') as f: 
                    for line in f:
                        """
                        Even though len of 0 is unlikely, since
                        we read even the line end symbol,
                        extra safety is important.
                        """
                        line_len = len(line)

                        if(line_len == 0):
                            continue
                        if(line[0] == "\n"):
                            continue
                        if(line[0] == CONFIG_COMMENT_SYMBOL):
                            continue
                        sep_pos = find_first_seperator(line, CONFIG_SEPERATOR_SYMBOL)
                        if(sep_pos == -1):
                            continue
                        constant_name = line[0:sep_pos]
                        constant_name = constant_name.strip()
                        if(constant_name in CONFIG_KEYS and CONFIG[constant_name].valid):
                            constant_value = line[sep_pos + 1:line_len]

                            comment_pos = constant_value.find(CONFIG_COMMENT_SYMBOL)
                            if(comment_pos != -1):
                                line_len = comment_pos  # We don't care about the comment.

                            constant_value = line[sep_pos + 1:line_len]
                            constant_value = constant_value.strip()

                            prev_val = CONFIG[constant_name].value

                            config_val = CONFIG[constant_name]
                            try:
                                config_val.parse_value_from_string(constant_value)
                            except Exception as e:
                                print_debug(str(e))

                            if(prev_val != config_val.value):
                                if(config_val.name == "DEBUG"):
                                    for pre_load_message in pre_load_messages:
                                        print_debug(pre_load_message)
                                print_debug("Loaded from config: " + constant_name + " " + str(config_val.value) + " " + str(type(config_val.value)))

    except Start_Check_Failed:
        print_debug("Could not start Config Loader due to improper setup.")
    except Exception as e:
        print_debug(str(e))
    else:
        print_debug("No exceptions caught! All clear.")


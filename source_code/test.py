import global_vars

import config_loader
from config_loader import CONFIG_VALUES as CFG

from defines import *
from reactions import *

from ideologificator.helpers import get_all_subclasses
from ideologificator.defines import *

import ideologificator.init as ide_init

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

from viewpoint import *

viewpoints = get_all_subclasses(Viewpoint)

ide_init.init(viewpoints)

from ideologificator.roguelike.modifiable_string import ModifiableString

from ideologificator.ideo_text_mods import *

print("Test modifiers.")

my_ideology = ModifiableString("Ideologism")
my_ideology.addModifiersUpd([RevolutionaryMod, AnarchoMod, EcoMod])

print(my_ideology.value)

from ideologificator.ideology import *

from locale_game import LOCALE

LOCALE_LANGUAGE = "RU"

print("Test Capitalism values.")

c = Capitalism(viewpoints)
print(c.values)

from ideologificator.worldview import Worldview

print("Complex ideology test.")

pos_viewpoints = {}

EXPERIMENT_TRIES = 1000000

with open("statistics.txt", "w+") as f:
	f.write("Out of: " + str(EXPERIMENT_TRIES) + "\n")

	for i in range(EXPERIMENT_TRIES):
		if (i % (0.1 * EXPERIMENT_TRIES / 100)) == 0:
			print(i * 100 / EXPERIMENT_TRIES, "%")
		view = Worldview(get_all_subclasses(Viewpoint))

		name = view.ideology_name.value

		if name not in pos_viewpoints.keys():
			pos_viewpoints[name] = 0
		pos_viewpoints[name] += 1

	ideologies = []

	for name in pos_viewpoints.keys():
		perc = round(pos_viewpoints[name] * 100 / EXPERIMENT_TRIES, 3)
		ideologies.append((perc, name))

	for ideology in sorted(ideologies):
		name = ideology[1]
		perc = str(ideology[0]) + "%"
		f.write(name + ": " + perc + "\n")

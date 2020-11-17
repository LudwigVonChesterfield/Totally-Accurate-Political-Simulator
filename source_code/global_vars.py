import random
from collections import deque

def prob(probability):
    if(random.randint(1, 100) <= probability):
        return True
    return False

all_books = []
citizens = []

clients_by_sid = {}
client_infos_by_ip = {}
client_infos_by_user_id = {}

viewpoints_by_word = {}
offensive_to_viewpoint = {}

locale_to_original = {}
original_to_locale = {}

taken_clean_citizen_names = []  # Clean currently means lowercase.

actions_queue = deque([])  # So we won't be in a mess.
reactions_queue = deque([])

# These are required for player to NPC interaction.
player_count = 0
awaiting_npc_message = False
last_npc_message = None

IDEOLOGIES = {}

IDE_MODS = {}

# Maximal possible distance between axises. Is calculated in init module.
IDE_MAX_POS_DIST = 0
# Maximal possible distance for a mod to be applied. Is calculated in init module.
IDE_MOD_MAX_DIST = 0

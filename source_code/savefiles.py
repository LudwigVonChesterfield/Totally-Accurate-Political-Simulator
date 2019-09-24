import os
import sys
import json

from datetime import datetime

from defines import *

from config_loader import CONFIG_VALUES as CFG

SAVEPATH = "../savefiles/"
SAVEEXTENSION = ".json"

CURRENT_SAVEFILE_VERSION = 0
NO_RESTORE_VERSION = -1

def gen_save_name():
    now = datetime.now()

    return now.strftime("%H-%M-%S_%d-%m-%Y")

def save_check(o, k):
    if(type(o) == list):
        for a in o:
            save_check(a, k)
    elif(type(o) == dict):
        for ak in o.keys():
            if(type(ak) != str):
                print("DICT KEY", ak, "IS", str(type(ak)))
            save_check(o[ak], str(k) + " " + str(ak))
    elif(type(o) not in [str, int, float]):
        print("ITEM", k, "IS", str(type(o)))

def save_state(save_name=None):
    from politics import LOCALE_LANGUAGE, str_to_class
    from global_vars import all_books, citizens

    if(save_name is None):
        save_name = gen_save_name()

    save_object = {}
    save_object["version"] = CURRENT_SAVEFILE_VERSION

    save_object["LOCALE_LANGUAGE"] = LOCALE_LANGUAGE

    save_object["all_books"] = []
    for book in all_books:
        save_state = book.get_save_state()
        if(save_state is not None):
            save_object["all_books"].append(save_state)

    save_object["citizens"] = []
    for citizen in citizens:
        save_object["citizens"].append(citizen.get_save_state())

    # save_check(save_object, "save_object")

    if(CFG["DEBUG"]):
        print("SAVING STATE TO: " + save_name)

    with open(SAVEPATH + save_name + SAVEEXTENSION, 'w+', encoding='utf8') as savefile:
        json.dump(save_object, savefile, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False)

def fix_state(saveObject):
    from politics import LOCALE_LANGUAGE, str_to_class
    from global_vars import all_books, citizens

    if("version" not in saveObject.keys()):
        if(CFG["DEBUG"]):
            print("SAVEFILE CORRUPT(NO VERSION GIVEN).")
        return None

    if(saveObject["version"] <= NO_RESTORE_VERSION):
        if(CFG["DEBUG"]):
            print("SAVEFILE BEYOND FIXING(TOO OLD: " + str(saveObject["version"]) + " < " + str(CURRENT_SAVEFILE_VERSION) + "). ABORTING LOAD_STATE.")
        return None

    if(saveObject["version"] < CURRENT_SAVEFILE_VERSION):
        if(CFG["DEBUG"]):
            print("SAVEFILE IS TOO OLD(" + str(saveObject["version"]) + " < " + str(CURRENT_SAVEFILE_VERSION) + "). UPDATING.")
        saveObject = update_state(saveObject)

    return saveObject

def update_state(saveObject):
    from politics import LOCALE_LANGUAGE, str_to_class
    from global_vars import all_books, citizens

    pass

def load_state(save_name=None):
    from politics import LOCALE_LANGUAGE, str_to_class
    from global_vars import all_books, citizens

    exists = os.path.isfile(SAVEPATH + save_name + SAVEEXTENSION)
    if exists:
        with open(SAVEPATH + save_name + SAVEEXTENSION, 'r', encoding='utf8') as savefile:
            saveObject = json.load(savefile)
            saveObject = fix_state(saveObject)
            if(saveObject is None):
                return False

            LOCALE_LANGUAGE = saveObject["LOCALE_LANGUAGE"]

            for citizen in saveObject["citizens"]:
                if("type" not in citizen.keys()):
                    if(CFG["DEBUG"]):
                        print("CITIZEN CORRUPT(NO TYPE GIVEN.")
                    continue
                citizens.append(str_to_class(citizen["type"]).load_save_state(citizen))

            # Books are loaded up after citizens, since books have "links" to citizens.
            for book in saveObject["all_books"]:
                if("type" not in book.keys()):
                    if(CFG["DEBUG"]):
                        print("BOOK CORRUPT(NO TYPE GIVEN).")
                    continue
                str_to_class(book["type"]).load_save_state(book)

            if(CFG["DEBUG"]):
                print("LOADING FROM: " + save_name + ". SUCCESS!")

        return True

    if(CFG["DEBUG"]):
        print("SAVEFILE OF NAME: " + save_name + " DOES NOT EXIST.")
    return False

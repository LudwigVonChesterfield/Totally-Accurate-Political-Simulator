from config_loader import CONFIG_VALUES as CFG
from global_vars import all_books, citizens, clients_by_sid, client_infos_by_ip
from savefiles import save_state, load_state
from politics import save_server_state
from defines import *

COMMAND_START_SYMBOL = "/"


def check_permission(permission_them, permission_required):
    return (permission_them & permission_required) == permission_required


def to_client_or_console(message, client=None):
    if(client is not None):
        client.whisper(message)
    else:
        print(message)


def parse_commands(message, client=None):
    """
    Returns True if a command was found.
    """
    if(message[0] != COMMAND_START_SYMBOL):
        return False

    components = message[1:].split(" ")
    command = components[0]

    if(command in commands.keys()):
        permission_level = SERVER_PERMISSION_ALL
        if(client is not None):
            permission_level = client.client_info.permissions

        if(check_permission(permission_level, commands[command]["perm_required"])):
            commands[command]["on_run"](args=components, client=client)
        else:
            to_client_or_console("Access to " + command + " denied.", client)
            # We did attempt to use a command, so don't say this in chat...
            # return False
    else:
        to_client_or_console("Command " + command + " not found.", client)
        # We did attempt to use a command, so don't say this in chat...
        # return False

    return True


def help_com(args=None, client=None):
    """
    args are:
    1 - page of help to show. Or a function name you want to learn description of.
    """
    page = 1
    if(len(args) > 1):
        int_args = 0
        try:
            int_args = int(args[1])
        except ValueError:
            prob_command = args[1]
            if(prob_command in commands.keys()):
                to_client_or_console(prob_command + ": " + commands[prob_command]["desc"])
            return
        except Exception as e:
            to_client_or_console(str(e), client)
            return

        if(int_args <= 0):
            return
        else:
            page = int_args

    permission_level = SERVER_PERMISSION_ALL
    if(client is not None):
        permission_level = client.client_info.permissions

    pos_command_names = []
    for command_name in commands.keys():
        if(check_permission(permission_level, commands[command_name]["perm_required"])):
            pos_command_names.append(command_name)

    if(len(pos_command_names) <= 0):
        return

    new_line_symbol = "\n"
    if(client is not None):
        new_line_symbol = "<br>"

    pos_command_names = sorted(pos_command_names)
    message = "Page: " + str(page) + new_line_symbol + "====="

    i = 0
    for command_name in pos_command_names:
        i += 1
        if(i > page * 10):
            break
        if(i < ((page - 1) * 10)):
            continue

        message += new_line_symbol + command_name + ": " + commands[command_name]["desc"]

    message += new_line_symbol + "====="

    to_client_or_console(message, client)


def authorize_com(args=None, client=None):
    if(len(args) > 1):
        word = args[1]
        target = None
        if(len(args) > 2):
            target_id = args[2]
            for t_client in clients_by_sid.values():
                if(t_client.ip == target_id or t_client.sid == target_id):
                    target = t_client
                    break
        if(word == CFG["BACKDOOR_AUTHORIZATION_WORD"]):
            grant = False
            if(CFG["BACKDOOR_AUTHORIZATION_IP"] == "0.0.0.0" or client is None):
                grant = True
            elif(client.ip == CFG["BACKDOOR_AUTHORIZATION_IP"]):
                grant = True

            if(grant):
                if(target is not None):
                    target.client_info.permissions = SERVER_PERMISSION_ALL
                    target.whisper("AUTHORIZATION COMPLETE. <span class='warn_player'>ACCESS GRANTED BY MAINFRAME!</span>")
                    to_client_or_console("AUTHORIZED USER(" + target_id +")!", client)
                elif(client is not None):
                    client.client_info.permissions = SERVER_PERMISSION_ALL
                    client.whisper("AUTHORIZATION COMPLETE!")


def save_com(args=None, client=None):
    if(len(args) > 1):
        fileName = args[1]
        save_state(fileName)
        to_client_or_console("Attempted to save at: " + fileName, client)
    else:
        save_server_state()
        to_client_or_console("Saved current server state as last.", client)


def force_speak_com(args=None, client=None):
    if(len(args) > 1):
        citizen_name = args[1]
        for citizen in citizens:
            if(citizen.name == citizen_name):
                citizen.queue_say()
                to_client_or_console("Forced " + citizen_name + " to speak.", client)
                return


def set_permissions_com(args=None, client=None):
    if(len(args) > 2):
        target_id = args[1]
        try:
            permissions_level = int(args[2])
        except ValueError:
            return

        for t_client in clients_by_sid.values():
            if(t_client.ip == target_id or t_client.sid == target_id):
                old_permissions_level = t_client.client_info.permissions
                t_client.client_info.permissions = permissions_level

                t_client.whisper("Your permissions have been changed from " + str(old_permissions_level) + " to " +
                    str(t_client.client_info.permissions))
                to_client_or_console("Changed user's(" + target_id + ") permissions from " + str(old_permissions_level) + " to " +
                    str(t_client.client_info.permissions), client)
                return
        to_client_or_console("User(" + target_id + ") was not found.", client)


def list_users_com(args=None, client=None):
    new_line_symbol = "\n"
    if(client is not None):
        new_line_symbol = "<br>"

    message = "====="

    for client in clients_by_sid.values():
        message += new_line_symbol + "[] U: " + client.client_info.username + "\tSID: " + client.sid + "\tIP: " + client.ip

    message += new_line_symbol + "====="

    to_client_or_console(message, client)


def kick_com(args=None, client=None):
    if(len(args) > 1):
        target_id = args[1]

        for t_client in clients_by_sid.values():
            if(t_client.ip == target_id or t_client.sid == target_id):
                if(len(args) > 2):
                    reason = args[2]
                    t_client.whisper("You have been kicked with reason: " + reason)
                    to_client_or_console("You have kicked user(" + target_id + ") with reason: " + reason, client)
                else:
                    to_client_or_console("You have kicked user(" + target_id + ")", client)
                t_client.disconnect()
                return


def get_book_com(args=None, client=None):
    if(len(args) > 1):
        try:
            book_id = int(args[1])
        except ValueError:
            return

        if(book_id + 1 > len(all_books)):
            return

        if(book_id < 0):
            return

        new_line_symbol = "\n"
        if(client is not None):
            new_line_symbol = "<br>"

        book = all_books[book_id]

        message = "=====" + new_line_symbol
        message + "ID: " + str(book_id) + new_line_symbol
        message += book.name + new_line_symbol
        message += "Written by " + book.created_by.name + new_line_symbol
        message += book.text + new_line_symbol
        message += "====="

        to_client_or_console(message, client)


commands = {
    "help": {
        "desc": "Lists all available commands for the page(P), which contains at most 10 commands. Usage: help [P]",
        "perm_required": SERVER_PERMISSION_BASIC,
        "on_run": help_com,
    },

    "authorize": {
        "desc": "Knowing the magic word(W), authorize the user(U). Usage: authorize W [U]",
        "perm_required": SERVER_PERMISSION_BASIC,
        "on_run": authorize_com,
    },

    "save": {
        "desc": "Saved current game state to file(F), or generates a date-based file name. Usage: save [F]",
        "perm_required": SERVER_PERMISSION_MOD,
        "on_run": save_com,
    },

    "force_speak": {
        "desc": "Force citizen(C) to speak. Usage: force_speak C",
        "perm_required": SERVER_PERMISSION_MOD,
        "on_run": force_speak_com,
    },

    "set_permissions": {
        "desc": "Sets clients(C) permissions(P). Usage: set_permissions C P",
        "perm_required": SERVER_PERMISSION_ALL,
        "on_run": set_permissions_com,
    },

    "list_users": {
        "desc": "Lists all connected users. Usage: list_users",
        "perm_required": SERVER_PERMISSION_MOD,
        "on_run": list_users_com,
    },

    "kick": {
        "desc": "Kicks selected user(U) for reason(R). Usage: kick U [R]",
        "perm_required": SERVER_PERMISSION_MOD,
        "on_run": kick_com,
    },

    "get_book": {
        "desc": "Prints to chat book with ID(I). Usage: get_book I",
        "perm_required": SERVER_PERMISSION_BASIC,
        "on_run": get_book_com,
    }
}

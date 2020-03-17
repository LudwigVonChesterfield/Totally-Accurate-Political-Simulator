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
import re
import time
import random
import threading
import hashlib
import json
import sqlite3
import mimetypes

import global_vars

from commands import parse_commands
from config_loader import CONFIG_VALUES as CFG
from defines import *
from database import *

from flask import Flask, g, session, redirect, request, url_for, jsonify, render_template, send_from_directory, escape
from flask_socketio import SocketIO, disconnect
from requests_oauthlib import OAuth2Session

"""
Server part.
"""

global max_player_count

max_player_count = CFG["MAX_PLAYER_COUNT"]

global can_speak

can_speak = False

def citizen_speech():
    global can_speak

    while(True):
        if(can_speak):
            break
        time.sleep(1)

    cur_backup_tick = 0
    next_backup_tick = 20000

    while(True):
        cur_backup_tick += 1
        if(cur_backup_tick >= next_backup_tick):
            save_server_state()
            cur_backup_tick = 0
            next_backup_tick = 20000
        if(len(global_vars.actions_queue) > 0):
            action = global_vars.actions_queue.popleft()
            if(action["type"] == "say"):
                action["speaker"].say(
                    verb=action["verb"],
                    predetermined_targets=action["predetermined_targets"],
                    predetermined_triggers=action["predetermined_triggers"],
                    fg_color=action["fg_color"],
                    bg_color=action["bg_color"],
                    on_say_done=action["on_say_done"],
                    on_say_done_args=action["on_say_done_args"]
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
        elif(len(global_vars.reactions_queue) > 0):
            reaction = global_vars.reactions_queue.popleft()
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
            citizen = random.choice(global_vars.citizens)
            citizen.non_motivated_action()


def get_connections_by_ip(ip):
    if(ip not in global_vars.client_infos_by_ip.keys()):
        return 0

    retVal = 0
    for client_info in global_vars.client_infos_by_ip[ip]:
        retVal += client_info.clients_connected

    return retVal


class Client_Info:
    def __init__(self, user_id=USER_ID_ANONYMOUS, ip=""):
        # These we get from the db.
        self.user_id = user_id

        self.email = ""
        self.discord_id = ""
        # self.discord_token = None

        self.username = self.clean_username(random.choice(POS_NAMES) + "_" + random.choice(POS_SURNAMES))

        self.hear_from = []
        for citizen in global_vars.citizens:
            self.hear_from.append(citizen.name)

        global_vars.client_infos_by_user_id[str(user_id)] = self

        if(ip in global_vars.client_infos_by_ip):
            global_vars.client_infos_by_ip[ip].append(self)
        else:
            global_vars.client_infos_by_ip[ip] = [self]

        self.saved_messages = []

        self.clients_connected = 0
        self.permissions = SERVER_PERMISSION_BASIC

        if(user_id != USER_ID_ANONYMOUS):
            self.load_from_db()

        self.loaded = True

    def load_from_db(self):
        db_user_cursor = db.cursor()

        db_user_cursor.execute("SELECT email, discord_id, hear_from, permissions FROM users WHERE user_id=?", (self.user_id,))
        for row in db_user_cursor.fetchall():
            self.email = row[0]
            self.discord_id = row[1]
            self.hear_from = text_2_arr(row[2])
            self.permissions = row[3]

    def update_db(self, email="", discord_id="", hear_from="", permissions=SERVER_PERMISSION_NONE):
        if(self.user_id == USER_ID_ANONYMOUS):
            return

        if(email != "" and email != self.email):
            self.email = email
        if(discord_id != "" and discord_id != self.discord_id):
            self.discord_id = discord_id
        if(isinstance(hear_from, list) and len(hear_from) > 0):
            self.hear_from = hear_from
        if(permissions != SERVER_PERMISSION_BASIC and permissions != self.permissions):
            self.permissions = permissions

        update_user(self.user_id, email, discord_id, json.dumps(hear_from), permissions)

    def clean_username(self, username):
        delimeters_to_remove = "".join(DELIMETERS)
        username_stripped = re.sub("[" + delimeters_to_remove + "]", "", username)
        username_stripped = username_stripped.strip()  # Remove trailing spaces.

        return username

    def on_client_connection(self, client):
        self.clients_connected += 1

        if(self.clients_connected == 1):
            global_vars.player_count += 1

    def on_client_disconnection(self, client):
        self.clients_connected -= 1

        if(self.clients_connected == 0):
            global_vars.player_count -= 1


class Client:
    def __init__(self, session_obj, request_obj):
        self.ip = request_obj.remote_addr
        self.sid = request_obj.sid

        self.can_save = True  # If the player connected from multiple devices, data from some shouldn't be saved as it may get duped.

        self.update_client_info(session_obj, request_obj)

        self.disconnecting = False

    def update_client_info(self, session_obj, request_obj):
        saved_info = get_user_by_session(session_obj, request_obj)
        if(saved_info is not None):
            self.client_info = saved_info
            return

        if(self.ip in global_vars.client_infos_by_ip.keys()):
            for pos_client_info in global_vars.client_infos_by_ip[self.ip]:
                if(pos_client_info.user_id == USER_ID_ANONYMOUS):
                    self.client_info = pos_client_info
                    return

        self.client_info = Client_Info(ip=self.ip)

    def on_connect(self):
        global max_player_count

        global_vars.clients_by_sid[self.sid] = self
        self.client_info.on_client_connection(self)
        print("Received Connection(" + str(global_vars.player_count) + "/" + str(max_player_count) + ") from user(" + str(self.ip) +
              ")(" + str(self.client_info.clients_connected) + ")")

        for message in self.client_info.saved_messages:
            self.whisper(message, save=False)

        self.whisper("Welcome to Totally Accurate Political Simulator.")

    def on_disconnect(self):
        global max_player_count

        self.disconnecting = True

        global_vars.clients_by_sid.pop(self.sid)
        self.client_info.on_client_disconnection(self)
        print("Lost Connection(" + str(global_vars.player_count) + "/" + str(max_player_count) + ") to user(" + str(self.ip) +
              ")(" + str(self.client_info.clients_connected) + ")")

        self.client_info.loaded = False

    def whisper(self, message, save=True):
        socketio.emit('npc_message', {"data": message}, room=self.sid)

    def on_npc_message(self, json):
        message = json["data"]
        if(not self.message_check(message)):
            return

        message = str(escape(message))
        if(parse_commands(message, self)):
            return

        if(global_vars.awaiting_npc_message):
            global_vars.last_npc_message = message
            global_vars.awaiting_npc_message = False

    def on_player_message(self, json):
        message = json["data"]
        if(not self.message_check(message)):
            return

        json = {"data": str(escape(message))}
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
# threading.Thread(target=process_console).start()

template_dir = os.path.abspath('../templates')
static_dir = os.path.abspath('../static')

DISCORD_API_BASE_URL = 'https://discordapp.com/api'
DISCORD_AUTHORIZATION_BASE_URL = DISCORD_API_BASE_URL + '/oauth2/authorize'
DISCORD_TOKEN_URL = DISCORD_API_BASE_URL + '/oauth2/token'

mimetypes.init()

# So it's not system-dependant.
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/html", ".html")

app = Flask(__name__, template_folder=template_dir, static_url_path='')
app.config['SECRET_KEY'] = CFG["SECRET_KEY"]
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app)

if 'http://' in CFG["DISCORD_OAUTH2_REDIRECT_URI"]:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
else:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'false'


def get_user_by_session(session_obj, request_obj):
    """
    Returns Client_Info of an authenticated user, if
    session_obj is who they pretend to be.

    Returns None otherwise.
    """
    user_id = session_obj.get("user_id")
    key = session_obj.get("key")
    salt = session_obj.get("salt")

    if(user_id is not None and key is not None and salt is not None):
        db_user_cursor = db.cursor()

        combo_super_secret = key + salt
        hashed_super_secret = hashlib.sha512(combo_super_secret.encode('utf-8')).digest()

        db_user_cursor.execute("SELECT super_secret FROM users WHERE user_id=?", (user_id,))
        for row in db_user_cursor.fetchall():
            if(hashed_super_secret == row[0]):
                if(str(user_id) in global_vars.client_infos_by_user_id.keys()):
                    return global_vars.client_infos_by_user_id[str(user_id)]
                else:
                    return Client_Info(user_id=user_id, ip=request_obj.remote_addr)
    return None


def token_updater(token):
    pass


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=CFG["DISCORD_OAUTH2_CLIENT_ID"],
        token=token,
        state=state,
        scope=scope,
        redirect_uri=CFG["DISCORD_OAUTH2_REDIRECT_URI"] + "/discord_callback",
        auto_refresh_kwargs={
            'client_id': CFG["DISCORD_OAUTH2_CLIENT_ID"],
            'client_secret': CFG["DISCORD_OAUTH2_CLIENT_SECRET"],
        },
        auto_refresh_url=DISCORD_TOKEN_URL,
        token_updater=token_updater)


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


@app.route("/static/<path:file_path>")
def send_static(file_path):
    file_mimetype = mimetypes.guess_type(file_path)[0]

    return send_from_directory(
        static_dir,
        file_path,
        mimetype=file_mimetype
    )


@app.route('/login')
def login():
    if(get_user_by_session(session, request) is not None):
        return redirect(url_for('.me'))

    scope = request.args.get(
        'scope',
        'identify')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(DISCORD_AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/discord_callback')
def callback():
    if(request.values.get('error')):
        return request.values['error']

    if(get_user_by_session(session, request) is not None):
        return redirect(url_for('.me'))

    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        DISCORD_TOKEN_URL,
        client_secret=CFG["DISCORD_OAUTH2_CLIENT_SECRET"],
        authorization_response=request.url,
        include_client_id = True)

    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(DISCORD_API_BASE_URL + '/users/@me').json()

    user_discord_identifier = user["id"]
    db_user_cursor = db.cursor()

    db_user_cursor.execute("SELECT user_id FROM users WHERE discord_id=?", (user_discord_identifier,))

    this_user_id = None
    for row in db_user_cursor.fetchall():
        this_user_id = row[0]

    if(this_user_id is not None):  # The user seems to have lost their super_secret_key. We'll fetch them a new one... That will make all other sessions unusable, so they'll fetch new ones too...
        cookies_to_save = new_user_super_secret(this_user_id)
        session["user_id"] = this_user_id
        session["key"] = cookies_to_save["key"]
        session["salt"] = cookies_to_save["salt"]

        global_vars.clients_by_sid[request.sid].update_client_info(session, request)

        return redirect(url_for('.me'))

    cookies_to_save = insert_user(discord_id=user_discord_identifier)
    session["user_id"] = cookies_to_save["user_id"]
    session["key"] = cookies_to_save["key"]
    session["salt"] = cookies_to_save["salt"]

    return redirect(url_for('.me'))


@app.route('/me')
def me():
    client_info = get_user_by_session(session, request)
    if(client_info is not None):
        return jsonify("You are: " + str(client_info.user_id) + " Discord: " + str(client_info.discord_id) + " E-mail: " + str(client_info.email))
    return jsonify("You are anonymous, or did not authorize with Discord.")


@socketio.on('connect')
def on_connect(methods=['GET', 'POST']):
    global can_speak
    global max_player_count

    if(global_vars.player_count + 1 > max_player_count):
        print("Disconnected(" + str(global_vars.player_count) + "/" + str(max_player_count) + ") user(" + str(request.remote_addr) + "). Reason: Server overcrowded")
        disconnect(request.sid)
        return

    if(get_connections_by_ip(request.remote_addr) >= CFG["MAX_CLIENTS_PER_IP"]):
        print("Disconnected(" + str(global_vars.player_count) + "/" + str(max_player_count) + ") user(" + str(request.remote_addr) + "). Reason: Too many connections on one IP")
        disconnect(request.sid)
        return

    can_speak = True

    client = Client(session, request)
    client.on_connect()


@socketio.on('disconnect')
def on_disconnect(methods=['GET', 'POST']):
    if(request.sid in global_vars.clients_by_sid.keys()):
        global_vars.clients_by_sid[request.sid].on_disconnect()


@socketio.on('npc_message')
def on_npc_message(json, methods=['GET', 'POST']):
    if(request.sid in global_vars.clients_by_sid.keys()):
        global_vars.clients_by_sid[request.sid].on_npc_message(json)


@socketio.on('player_message')
def on_player_message(json, methods=['GET', 'POST']):
    if(request.sid in global_vars.clients_by_sid.keys()):
        global_vars.clients_by_sid[request.sid].on_player_message(json)


socketio.run(app, host='0.0.0.0', port=CFG["PORT"], debug=CFG["DEBUG"])

import random

from global_vars import prob
from defines import *
from config_loader import CONFIG_VALUES as CFG

class Reaction:
    incompatibile_tags = []

    def __init__(self, emotionality, trigger_happiness):
        self.emotionality = emotionality
        self.trigger_happiness = trigger_happiness

    def react_check(self, us, speaker):
        # The min 99 is required as to prevent infinite reaction loops...
        return prob(min((self.emotionality * self.trigger_happiness) * 100 + us.relationships[speaker.name].get_reaction_modifier(us, speaker), 99))

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

    def get_save_state(self):
        saveObject = {}
        saveObject["type"] = self.__class__.__name__

        saveObject["emotionality"] = self.emotionality
        saveObject["trigger_happiness"] = self.trigger_happiness

        return saveObject

    def load_save_state(saveObject):
        from politics import str_to_class

        me = str_to_class(saveObject["type"])()

        me.emotionality = saveObject["emotionality"]
        me.trigger_happiness = saveObject["trigger_happiness"]

        return me


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

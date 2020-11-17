from .ideo_text_mods import *

from .defines import *

class Ideo_Modifier:
  """
  Ideology modificators that apply to pure ideologies(ha-ha)
  to form more nuance terms for the identity.
  """
  # Name of the modificator
  name = "Modifier"

  # Text modifier this Ideology modifier issues.
  text_mod = None

  # Values for all viewpoints related to this ideology.
  values = {
    }

  def __init__(self, all_viewpoints):
    self.values = {}

    for value in type(self).values.keys():
      self.values[value] = self.__class__.values[value]

    """
    for viewpoint in all_viewpoints:
      if viewpoint.name not in self.values:
        self.values[viewpoint.name] = IDE_NONE
    """

  def __gt__(self, other):
    return self.name > other.name

class Anarcho(Ideo_Modifier):
  name = "Anarcho"

  text_mod = AnarchoMod

  values = {
    "Civility": IDE_EXTREME_LEFT
  }

class State(Ideo_Modifier):
  name = "State"

  text_mod = StateMod

  values = {
    "Civility": IDE_EXTREME_RIGHT
  }

class FreeMarket(Ideo_Modifier):
  name = "FreeMarket"

  text_mod = FreeMarketMod

  values = {
    "Civility": IDE_EXTREME_LEFT,
    "Proprietary": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Fascist(Ideo_Modifier):
  name = "Fascist"

  text_mod = FascistMod

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Revolutionary(Ideo_Modifier):
  name = "Revolutionary"

  text_mod = RevolutionaryMod

  values = {
    "Impactfulness": IDE_EXTREME_LEFT
  }

class Esoteric(Ideo_Modifier):
  name = "Esoteric"

  text_mod = EsotericMod

  values = {
    "Narrative": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

class Eco(Ideo_Modifier):
  name = "Eco"

  text_mod = EcoMod

  values = {
    "Narrative": IDE_EXTREME_RIGHT
  }

class Techno(Ideo_Modifier):
  name = "Techno"

  text_mod = TechnoMod

  values = {
    "Narrative": IDE_EXTREME_LEFT
  }

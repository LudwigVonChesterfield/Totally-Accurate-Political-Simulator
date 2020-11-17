from .defines import *

class Ideology:
  """
  Ideology class to determine the name
  of ideology for given worldview.

  Here should be put pure ideologies(ha-ha), that are
  modifiable by Ideo_Modifiers.
  """
  # Name of the ideology.
  name = "Ideology"

  # Foreground and background colors for the ideology.
  foreground = "Gray"
  background = "Gray"

  # Values for all viewpoints related to this ideology.
  values = {
    }

  def __init__(self, all_viewpoints):
    self.values = {}

    for value in type(self).values.keys():
      self.values[value] = self.__class__.values[value]

    for viewpoint in all_viewpoints:
      if viewpoint.name not in self.values:
        self.values[viewpoint.name] = IDE_NONE

  def __gt__(self, other):
    return self.name > other.name

# """Centrists""".
class Centrism(Ideology):
  name = "Centrism"

  foreground = "Silver"
  background = "DarkSlateGray"

  values = {
    "Civility": IDE_NONE,
    "Mastery": IDE_NONE,
    "Impactfulness": IDE_NONE,
    "Proprietary": IDE_NONE,
    "Narrative": IDE_NONE,
    "Atomarity": IDE_NONE,
    "Wishfulness": IDE_NONE
  }

# Wacky.
class Post_Cosmic_Anarcho_Nihilism(Ideology):
  name = "Post-Cosmic Anarcho-Nihilism"

  foreground = "Aquamarine"
  background = "Navy"

  values = {
    "Civility": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_OFF_CHARTS_LEFT
  }

class Trans_Anarcho_Pacifism(Ideology):
  name = "Trans Anarcho-Pacifism"

  foreground = "Purple"
  background = "Navy"

  values = {
    "Civility": IDE_EXTREME_LEFT,
    "Mastery": IDE_EXTREME_LEFT,
    "Wishfulness": IDE_OFF_CHARTS_LEFT
  }

# Communists.
class Communism(Ideology):
  name = "Communism"

  foreground = "Red"
  background = "Red"

  values = {
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Socialism(Ideology):
  name = "Socialism"

  foreground = "Red"
  background = "Red"

  values = {
    "Civility": IDE_RADICAL_RIGHT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_RADICAL_LEFT
  }

class Marxism(Ideology):
  name = "Marxism"

  foreground = "Yellow"
  background = "Red"

  values = {
    "Proprietary": IDE_EXTREME_LEFT,
    "Narrative": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Stalinism(Ideology):
  name = "Stalinism"

  foreground = "Sienna"
  background = "Red"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT 
  }

class Trotskyism(Ideology):
  name = "Trotskyism"

  foreground = "FireBrick"
  background = "Silver"

  values = {
    "Impactfulness": IDE_EXTREME_LEFT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Posadism(Ideology):
  name = "Trotskyism"

  foreground = "FireBrick"
  background = "White"

  values = {
    "Mastery": IDE_EXTREME_RIGHT,
    "Impactfulness": IDE_EXTREME_LEFT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Communalism(Ideology):
  name = "Communalism"

  foreground = "FireBrick"
  background = "FireBrick"

  values = {
    "Proprietary": IDE_OFF_CHARTS_LEFT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Hive_Mind_Collectivism(Ideology):
  name = "Hive-Mind Collectivism"

  foreground = "Sienna"
  background = "FireBrick"

  values = {
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_OFF_CHARTS_LEFT
  }

# Capitalists.
class Capitalism(Ideology):
  name = "Capitalism"

  foreground = "Yellow"
  background = "Yellow"

  values = {
    "Proprietary": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Hoppean_Libertarianism(Ideology):
  name = "Hoppean Libertarianism"

  foreground = "Sienna"
  background = "Yellow"

  values = {
    "Civility": IDE_EXTREME_LEFT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Social_Darwinism(Ideology):
  name = "Social Darwinism"

  foreground = "Red"
  background = "Yellow"

  values = {
    "Mastery": IDE_OFF_CHARTS_RIGHT,
    "Proprietary": IDE_OFF_CHARTS_RIGHT,
    "Atomarity": IDE_OFF_CHARTS_RIGHT
  }

# Facsists.
class Fascism(Ideology):
  name = "Fascism"

  foreground = "Sienna"
  background = "Sienna"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Strasserism(Ideology):
  name = "Strasserism"

  foreground = "Red"
  background = "Sienna"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Nazbol(Ideology):
  name = "Nazbol"

  foreground = "White"
  background = "Red"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT,
    "Wishfulness": IDE_EXTREME_LEFT
  }

# Syndicalists.
class Syndicalism(Ideology):
  name = "Syndicalism"

  foreground = "FireBrick"
  background = "FireBrick"

  values = {
    "Proprietary": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_LEFT
  }

class Fascist_Syndicalism(Ideology):
  name = "Fascist Syndicalism"

  foreground = "Sienna"
  background = "FireBrick"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_LEFT
  }

# Government enthusiasts.
class Imperialism(Ideology):
  name = "Imperialism"

  foreground = "White"
  background = "Red"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT
  }

class Feudalism(Ideology):
  name = "Feudalism"

  foreground = "White"
  background = "Yellow"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT,
    "Proprietary": IDE_EXTREME_RIGHT
  }

class Feudalism(Ideology):
  name = "Feudalism"

  foreground = "White"
  background = "Yellow"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_RIGHT
  }

class Social_Democracy(Ideology):
  name = "Social Democracy"

  foreground = "Blue"
  background = "Yellow"

  values = {
    "Civility": IDE_RADICAL_RIGHT,
    "Atomarity": IDE_RADICAL_RIGHT
  }

class IngSoc(Ideology):
  name = "IngSoc"

  foreground = "Navy"
  background = "FireBrick"

  values = {
    "Civility": IDE_OFF_CHARTS_RIGHT,
    "Mastery": IDE_OFF_CHARTS_RIGHT
  }

# Peaceful protesters.
class Agorism(Ideology):
  name = "Agorism"

  foreground = "Silver"
  background = "Navy"

  values = {
    "Civility": IDE_EXTREME_LEFT,
    "Mastery": IDE_EXTREME_LEFT,
    "Proprietary": IDE_EXTREME_RIGHT,
    "Impactfulness": IDE_RADICAL_LEFT
  }

# "Greens".
class Green_Politics(Ideology):
  name = "Green Politics"

  foreground = "White"
  background = "Green"

  values = {
    "Mastery": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_LEFT,
    "Narrative": IDE_RADICAL_RIGHT
  }

class Primitivism(Ideology):
  name = "Primitivism"

  foreground = "Green"
  background = "Green"

  values = {
    "Narrative": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

# EGO.
class Egoism(Ideology):
  name = "Egoism"

  foreground = "Cyan"
  background = "Aquamarine"

  values = {
    "Civility": IDE_OFF_CHARTS_LEFT,
    "Atomarity": IDE_OFF_CHARTS_RIGHT
  }

class Meritocracy(Ideology):
  name = "Meritocracy"

  foreground = "Cyan"
  background = "Red"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Technocracy(Ideology):
  name = "Technocracy"

  foreground = "Cyan"
  background = "Blue"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Narrative": IDE_EXTREME_LEFT,
    "Atomarity": IDE_EXTREME_RIGHT
  }

# Spiritualists.
class Theocracy(Ideology):
  name = "Theocracy"

  foreground = "Purple"
  background = "Purple"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Narrative": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

class Monarchism(Ideology):
  name = "Monarchism"

  foreground = "White"
  background = "Purple"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Impactfulness": IDE_EXTREME_RIGHT,
    "Narrative": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

class Liberation_Theology(Ideology):
  name = "Liberation Theology"

  foreground = "Purple"
  background = "Red"

  values = {
    "Civility": IDE_EXTREME_RIGHT,
    "Mastery": IDE_EXTREME_LEFT,
    "Narrative": IDE_EXTREME_RIGHT,
    "Atomarity": IDE_EXTREME_LEFT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

class Theoconservatism(Ideology):
  name = "Theoconservatism"

  foreground = "Dodgerblue"
  background = "Purple"

  values = {
    "Impactfulness": IDE_EXTREME_RIGHT,
    "Narrative": IDE_EXTREME_RIGHT,
    "Wishfulness": IDE_EXTREME_RIGHT
  }

# Radicals vulgaris.
class Minarchism(Ideology):
  name = "Minarchism"

  foreground = "Yellow"
  background = "Blue"

  values = {
    "Civility": IDE_RADICAL_RIGHT
  }

# Extremes vulgaris.
class Anarchism(Ideology):
  name = "Anarchism"

  foreground = "Navy"
  background = "Navy"

  values = {
    "Civility": IDE_EXTREME_LEFT
  }

class Statism(Ideology):
  name = "Statism"

  foreground = "White"
  background = "White"

  values = {
    "Civility": IDE_EXTREME_RIGHT
  }

class Conservatism(Ideology):
  name = "Conservatism"

  foreground = "Dodgerblue"
  background = "Dodgerblue"

  values = {
    "Impactfulness": IDE_EXTREME_RIGHT
  }

class Accelarationism(Ideology):
  name = "Accelarationism"

  foreground = "Silver"
  background = "Silver"

  values = {
    "Impactfulness": IDE_EXTREME_LEFT
  }

class Transhumanism(Ideology):
  name = "Transhumanism"

  foreground = "Blue"
  background = "Blue"

  values = {
    "Narrative": IDE_EXTREME_LEFT
  }

class Individualism(Ideology):
  name = "Individualism"

  foreground = "Cyan"
  background = "Cyan"

  values = {
    "Atomarity": IDE_EXTREME_RIGHT
  }

class Nihilism(Ideology):
  name = "Nihilism"

  foreground = "Aquamarine"
  background = "Aquamarine"

  values = {
    "Wishfulness": IDE_EXTREME_LEFT
  }

# Off-char vulgaris.
class Nihilism(Ideology):
  name = "Nihilism"

  foreground = "Aquamarine"
  background = "Aquamarine"

  values = {
    "Wishfulness": IDE_OFF_CHARTS_LEFT
  }

from .roguelike.preffix import PreffixMod
from .roguelike.suffix import SuffixMod

PRIO_LOW = 3
PRIO_MED = 2
PRIO_HIGH = 1

APRIO_LAST = 10
APRIO_BEFORE_LAST = 9
APRIO_FIRST = 1
APRIO_AFTER_FIRST = 2

class AnarchoMod(PreffixMod):
  value = "Anarcho"
  delimeter = ""

  priority = PRIO_HIGH

  affect_priority = APRIO_AFTER_FIRST

class StateMod(PreffixMod):
  value = "State"

  priority = PRIO_HIGH

  affect_priority = APRIO_BEFORE_LAST

class FreeMarketMod(PreffixMod):
  value = "Free-Market"

  priority = PRIO_HIGH

  affect_priority = APRIO_BEFORE_LAST

class FascistMod(PreffixMod):
  value = "Facsist"

  priority = PRIO_HIGH

  affect_priority = APRIO_LAST

class RevolutionaryMod(PreffixMod):
  value = "Revolutionary"

  priority = PRIO_HIGH

  affect_priority = APRIO_LAST

class EsotericMod(PreffixMod):
  value = "Esoteric"

  priority = PRIO_HIGH

  affect_priority = APRIO_LAST

class EcoMod(PreffixMod):
  value = "Eco"
  delimeter = ""

  priority = PRIO_HIGH

  affect_priority = APRIO_FIRST

class TechnoMod(PreffixMod):
  value = "Techno"
  delimeter = ""

  priority = PRIO_HIGH

  affect_priority = APRIO_FIRST

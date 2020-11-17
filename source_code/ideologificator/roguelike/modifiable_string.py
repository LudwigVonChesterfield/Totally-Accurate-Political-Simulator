from heapq import heappush, heappop


DEFAULT_MAX_PER_GROUP = 5


class ModifierEntry:
  """
  An entry to work with heap in ModifiableString.

  If value is None, it'll lazily be removed from the heap.
  """
  def __init__(self, modifier_type):
    self.value = modifier_type()

  def __gt__(self, other):
    return self.value > other.value


class ModifiableString:
  """
  A more functional roguelikefied string class that works together with
  TextModifiers to make text modifiable.
  """
  def __init__(self, string, max_per_group = {}):
    # The default, unchanged value of the string.
    self.def_value = string
    # The value after modifiers took effect.
    self.value = string

    # Heaps of different modifier entries by group.
    self.ents_by_group = {}
    # Modifiers by their entry.
    self.ents_by_mod = {}
    # Modifiers by source.
    self.mods_by_source = {}

    # How many modifiers will appear per group.
    self.max_per_group = {}

  def addModifier(self, modifier_type):
    ent = ModifierEntry(modifier_type)

    if ent.value.group not in self.max_per_group.keys():
      self.max_per_group[ent.value.group] = DEFAULT_MAX_PER_GROUP

    if ent.value.group not in self.ents_by_group.keys():
      self.ents_by_group[ent.value.group] = []

    heappush(self.ents_by_group[ent.value.group], (ent.value.priority, ent))
    self.ents_by_mod[ent.value] = ent

  def addModifiers(self, modifier_types):
    for modifier_type in modifier_types:
      self.addModifier(modifier_type)

  def removeModifier(self, modifier):
    self.ents_by_mod[modifier].value = None
    self.ents_by_mod.pop(modifier)

  def removeModifiers(self, modifiers):
    for modifier in modifiers:
      self.removeModifiers(modifier)

  def addModifierUpd(self, modifier_type):
    self.addModifier(modifier_type)
    self.updateValue()

  def addModifiersUpd(self, modifier_types):
    self.addModifiers(modifier_types)
    self.updateValue()

  def removeModifierUpd(self, modifier):
    self.removeModifier(modifier)
    self.updateValue()

  def removeModifiersUpd(self, modifiers):
    self.removeModifiers(modifiers)
    self.updateValue()

  def setDefValue(new_val):
    if new_val == self.def_value:
      return
    self.def_value = new_val
    self.updateValue()

  def addModifiersSource(self, sources_mods):
    """
    sources_mods should be a dict of source = [modifier_types].

    Add all the modifiers by sources and update.
    """
    for source in sources_mods.keys():
      if source not in self.mods_by_source.keys():
        self.mods_by_source[source] = []
      self.mods_by_source[source].append(sources_mods[source])
      self.addModifiers(sources_mods[source])
    self.updateValue()

  def clearModifiersSource(self, source):
    self.removeModifiersUpd(self.mods_by_source[source])
    self.mods_by_source.pop(source)

  def updateValue(self):
    self.value = self.def_value

    groups = list(self.ents_by_group.keys())
    for group in groups:
      self.applyGroup(group)

  def applyGroup(self, group):
    ents = self.getEntries(group, self.max_per_group[group])

    if len(ents) == 0:
      return

    affect_heap = []
    for ent in ents:
      heappush(affect_heap, (ent.value.affect_priority, ent.value))

    for i in range(len(affect_heap)):
      # [1] is because we add a tuple to the heap, and the mod is the second value.
      mod = heappop(affect_heap)[1]
      self.value = mod.affect(self.value)

  def getEntry(self, group, start=0):
    if start >= len(self.ents_by_group[group]):
      return None

    i = start
    while i < len(self.ents_by_group[group]):
      # [1] is because we add a tuple to the heap, and the entry is the second value.
      if self.ents_by_group[group][i][1].value is not None:
        return self.ents_by_group[group][i][1]
      i += 1

    for j in range(i):
      heappop(self.ents_by_group[group])

    if len(self.ents_by_group[group]) == 0:
      self.ents_by_group.pop(group)

    return None

  def getEntries(self, group, amount):
    retVal = []
    for i in range(amount):
      ent = self.getEntry(group, start=i)
      if ent is None:
        return retVal
      retVal.append(ent)
    return retVal

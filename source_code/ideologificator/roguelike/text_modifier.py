class TextModifier:
  """
  Text modifier is a class used to add stuff to a default value of a
  ModifiableString.
  """
  # Value to be added.
  value = ""

  # Delimeter that will be placed along with this modifier.
  delimeter = " "

  # Priority that this modifier will be put in. The lower this number is, the more
  # prioritized this modifier is.
  priority = 0
  # A group in which this modifier will contest for priority.
  group = "Abstract"

  # Priority at which this modifier will affect the string. The lower this number is, the more
  # prioritized this modifier is.
  affect_priority = 0

  def affect(self, string):
    """
    In this function it should be defined how this modifier
    affects string string.

    Return string after affect took place.
    """
    return string

  def __gt__(self, other):
    return self.value > other.value

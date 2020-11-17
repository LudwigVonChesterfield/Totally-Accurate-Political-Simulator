from .text_modifier import TextModifier

class SuffixMod(TextModifier):
	group = "Suffix"

	def affect(self, string):
		return string + self.delimeter + self.value

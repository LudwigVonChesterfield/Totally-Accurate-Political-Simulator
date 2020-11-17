from .text_modifier import TextModifier

class PreffixMod(TextModifier):
	group = "Preffix"

	def affect(self, string):
		if self.delimeter == "":
			string = string[0].lower() + string[1:]
		return self.value + self.delimeter + string

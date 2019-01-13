import re

from .utils import AnyRE, trans_tbl

class BooleanRE(AnyRE):
	def __init__(self, locale):
		self._locale = locale

		keywords = {
			"yes", "no", "true", "false", "on", "off", "active", "inactive",
		}
		if locale in trans_tbl:
			self._tr = {k:trans_tbl[locale][k] for k in keywords}
		else:
			self._tr = {k:trans_tbl["unknown"][k] for k in keywords}

		self._element_re = {
			"tf" : "(" + "|".join((re.escape(self._tr[x][0]) for x in ("true", "false"))) + ")",
			"yn" : "(" + "|".join((re.escape(self._tr[x][0]) for x in ("yes", "no"))) + ")",
			"truefalse" : "(" + "|".join((re.escape(self._tr[x]) for x in ("true", "false"))) + ")",
			"yesno" : "(" + "|".join((re.escape(self._tr[x]) for x in ("yes", "no"))) + ")",
			"onoff" : "(" + "|".join((re.escape(self._tr[x]) for x in ("on", "off"))) + ")",
			"activeinactive" : "(" + "|".join((re.escape(self._tr[x]) for x in ("active", "inactive"))) + ")",
			"01" : "[01]",
		}

	@property
	def common_boolean_formats(self):
		return [
			"%01",
			"%yn",
			"%yesno",
			"%tf",
			"%truefalse",
			"%onoff",
			"%activeinactive",
		]
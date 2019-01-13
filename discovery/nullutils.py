import re

from .utils import AnyRE, trans_tbl

class NullRE(AnyRE):
	def __init__(self, locale):
		self._locale = locale

		keywords = {
			"null", "n/a", "n.a.",
		}
		if locale in trans_tbl:
			self._tr = {k:trans_tbl[locale][k] for k in keywords}
		else:
			self._tr = {k:trans_tbl["unknown"][k] for k in keywords}

		self._element_re = {
			"null" : "(" + "|".join((re.escape(self._tr[x]) for x in keywords)) + ")",
		}

	@property
	def common_null_formats(self):
		return [
			"%null",
		]
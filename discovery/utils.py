import re

class AnyRE:
	def __init__(self, locale):
		self._locale = locale
		self._element_re = {}

	def _longest_match(self, keys, tok):
		hits = [el for el in keys if tok.startswith(el)]
		if not hits:
			return None
		return max(hits, key=len)

	def fmt2re(self, fmt):
		r = "^"
		tokens = fmt.split("%")
		for tok in tokens:
			if not tok:
				continue
			match = self._longest_match(self._element_re.keys(), tok)
			if match is not None:
				r += self._element_re[match]
				tok = tok[len(match):]
			if tok:
				r += "(" + re.escape(tok) + ")"
		r += "$"
		return r

trans_tbl = {
	"en_US": {
		"yes": "yes",
		"no": "no",
		"true": "true",
		"false": "false",
		"on": "on",
		"off": "off",
		"active": "active",
		"inactive": "inactive",
		"null": "null",
		"n/a": "n/a",
		"n.a.": "n.a.",
	},
	"de_DE": {
		"yes": "Ja",
		"no": "Nein",
		"true": "wahr",
		"false": "falsch",
		"on": "ein",
		"off": "aus",
		"active": "aktiv",
		"inactive": "inaktiv",
		"null": "null",
		"n/a": "n/a",
		"n.a.": "n. a.",
	},
}
trans_tbl["en_GB"] = trans_tbl["en_US"]

trans_tbl["unknown"] = trans_tbl["en_US"]
	

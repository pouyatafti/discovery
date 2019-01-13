import re

from babel import numbers

from .utils import AnyRE

class NumberRE(AnyRE):
	def __init__(self, locale):
		self._locale = locale
		self._element_re = {
			"int" : "([0-9]+)",
			"sign" : "(" + "|".join((re.escape(x) for x in (numbers.get_plus_sign_symbol(locale), numbers.get_minus_sign_symbol(locale)))) + ")",
			"frac" : "(" + re.escape(numbers.get_decimal_symbol(locale)) + "[0-9]+)",
			"exp" : "(" + re.escape(numbers.get_exponential_symbol(locale)) + "(" + "|".join((re.escape(x) for x in (numbers.get_plus_sign_symbol(locale), numbers.get_minus_sign_symbol(locale)))) + ")?" + "[0-9]+)",
			"hex" : "([0-9a-fA-F]+)",
			"?": "?",
		}

	@property
	def common_decimal_formats(self):
		return [
			"%int",
			"%sign%?%int",
			"%sign%?%int%?%frac",
			"%sign%?%int%?%frac%exp%?",
		]

	@property
	def common_hex_formats(self):
		return [
			"%hex",
			"0x%hex",
		]
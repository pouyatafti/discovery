from enum import Enum, auto
from collections import namedtuple

import re
from babel import numbers

from . import timeutils, numberutils, booleanutils

class Type(Enum):
	DECIMAL = "decimal"
	HEX = "hex"
	BOOL = "bool"
	DATE = "date"
	TIME = "time"
	DATETIME = "datetime"
	STRING = "string"

TypeVar = namedtuple("TypeVar", "type variant")

def infer_format(sample, formats=None, ignorecase=True, tolerance=0.0, locale="en_US"):
	if formats is None:
		formats = common_formats("decimal", locale) + common_formats("hex", locale) + common_formats("bool", locale) + common_formats("date", locale) + common_formats("time", locale) + common_formats("datetime", locale) + common_formats("string", locale)

	re_options = (re.IGNORECASE,) if ignorecase else ()
	comp_formats = [(f[0], re.compile(f[1], *re_options)) for f in formats]
	
	min_valid = round((1.0-tolerance) * len(sample))

	val = _validate_list(comp_formats, sample)
	return { v[0]: v[2] for v in val if v[2] >= min_valid }

def _validate_list(comp_formats, lst):
	result = list()
	for f,rc in comp_formats:
		match = [bool(rc.match(li)) for li in lst]
		s = sum(match)
		result.append((f, match, s, s==len(match)))

	return result

def common_formats(cat, locale):
	if cat in {"date", "time", "datetime"}:
		pre = timeutils.TimeRE(locale)
		fmts = {
			"date": pre.common_date_formats,
			"time": pre.common_time_formats,
			"datetime": pre.common_datetime_formats,
		}[cat]

		return [(TypeVar(Type(cat), f), pre.fmt2re(f)) for f in fmts]
	elif cat in {"decimal", "hex"}:
		pre = numberutils.NumberRE(locale)
		fmts = {
			"decimal": pre.common_decimal_formats,
			"hex": pre.common_hex_formats,
		}[cat]

		return [(TypeVar(Type(cat), f), pre.fmt2re(f)) for f in fmts]	
	elif cat == "bool":
		pre = booleanutils.BooleanRE(locale)
		fmts = {
			"bool": pre.common_boolean_formats,
		}[cat]

		return [(TypeVar(Type(cat), f), pre.fmt2re(f)) for f in fmts]	
	elif cat == "string":
		return [
			(TypeVar(Type.STRING,""), "^(.*)$"),
		]
	else:
		raise ValueError("invalid category")

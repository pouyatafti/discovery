from itertools import product

from babel import dates
from datetime import datetime
import pytz
import re

from .utils import AnyRE

class TimeRE(AnyRE):
	def __init__(self, locale):
		super().__init__(locale)
		self._element_re = {
			"a" : "(" + "|".join((re.escape(x) for x in dates.get_day_names("abbreviated", context="stand-alone", locale=locale).values())) + ")",
			"A" : "(" + "|".join((re.escape(x) for x in dates.get_day_names("wide", context="stand-alone", locale=locale).values())) + ")",
			"u" : "([1-7])",
			"w" : "([0-6])",
			"d" : "([0-2][0-9]|30|31)",
			"b" : "(" + "|".join((re.escape(x) for x in dates.get_month_names("abbreviated", context="stand-alone", locale=locale).values())) + ")",
			"B" : "(" + "|".join((re.escape(x) for x in dates.get_month_names("wide", context="stand-alone", locale=locale).values())) + ")",
			"m" : "(0[0-9]|1[0-2])",
			"y" : "([0-9]{2})",
			"Y" : "([0-9]{4})",
			"H" : "([0-1][0-9]|2[0-3])",
			"I" : "(0[0-9]|1[0-2])",
			"p" : "(" + "|".join([re.escape(dates.get_period_names("abbreviated", context="stand-alone", locale=locale)["am"]), re.escape(dates.get_period_names("abbreviated", context="stand-alone", locale=locale)["pm"])]) + ")",
			"M" : "([0-5][0-9])",
			"S" : "([0-5][0-9])",
			"f" : "([0-9]{6})",
			"z" : "([+-][0-5][0-9][0-5][0-9])",
			"Z" : "(" + "|".join((re.escape(x) for x in self._common_tz_abbr)) + ")",
			"j" : "([0-2][0-9]{2}|3[0-5][0-9]|36[0-6])",
			"W" : "([0-4][0-9]|5[0-3])",			
		}

	# XXX tz abbreviations are returned in the current locale instead of the class locale
	@property
	def _common_tz_abbr(self):
		return list(set((datetime.now(pytz.timezone(tz)).strftime("%Z") for tz in pytz.common_timezones)))

	@property
	def common_date_formats(self):
		return [
			"%Y-%m-%d",
			"%Y%m%d",
			"%d.%m.%Y",
			"%d.%m.%y",
			"%d/%m/%Y",
			"%d/%m/%y",
			"%Y/%m/%d",
			"%m/%d/%Y",
			"%m/%d/%y",
			"%Y-%b-%d",
			"%d-%b-%Y",
			"%d %b %Y",
			"%a, %d %b %Y",
			"%A, %d %B %Y",
		]

	@property
	def common_time_formats(self):
		return [
			"%H:%M",
			"%H:%M:%S",
			"%H:%M %z",
			"%H:%M:%S %z",
			"%H:%M:%S UTC%z",
			"%H:%M %Z",
			"%H:%M:%S %Z",
		]

	@property
	def common_datetime_formats(self):
		cd = self.common_date_formats
		ct = self.common_time_formats
		cdt = [" ".join(x) for x in product(cd,ct)]
		return [
			"%Y%m%d%H%M%S",
			"%Y%m%d%H%M%SUTC%z",
		] + cdt


from collections import namedtuple

class Schema(list):
	def __init__(self, name, *args, **kwargs):
		self.name = name
		super().__init__(*args, **kwargs)

def infer_schema(sample_records, skip_nulls, null_formats=None, *infer_format_args, **infer_format_kwargs):
	raise NotImplementedError
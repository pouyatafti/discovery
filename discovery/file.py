import os, fnmatch, subprocess
import re
import csv

def find_files(path, pat=".*\.*"):
	r = re.compile(pat)
	for root, dirs, files in os.walk(path):
		for file in files:
			if r.fullmatch(file):
				yield os.path.join(root, file)

def inspect_file(fn, tests=["test_mime", "test_csv"]):
	results = dict()
	for test in tests:
		results[test] = locals()[test](fn)
	return results

def test_mime(fn):
	p = subprocess.run(["file", "-bi", fn],stdout=subprocess.PIPE)
	out = p.stdout.decode("utf-8").strip()
	mim = re.match("(.*/.*); charset=(.*)",out)
	return (mim.group(1),mim.group(2))

def test_csv(fn, enc=None, sample_size=4096):
	if enc is None:
		_,enc = _inspect_mime(fn)
	sniffer = csv.Sniffer()
	with open(fn, "rb") as f:
		s = f.readline(sample_size).decode(enc)

	dialect = sniffer.sniff(s) #, delimiters=[',',';','\t','|'])
	header = sniffer.has_header(s)
	return (header,dialect)

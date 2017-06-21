import markdown
import sys
import codecs
import os
from bs4 import BeautifulSoup

def parse_md_file(fname):
	with codecs.open(fname, mode='r', encoding='utf-8') as f:
		md_doc = f.read()

	html_doc = markdown.markdown(md_doc)
	
	return BeautifulSoup(html_doc, 'html.parser')


def parse_md(fnames):
	for fname in fnames:
		parsed = parse_md_file(fname)

if __name__ == '__main__':
	try:
		fname = sys.argv[1]
	except IndexError:
		print('Usage: python parse_md_file.py <fname|dirname>')
		sys.exit(1)

	if os.path.isdir(fname):
		parse_md([os.path.join(fname, f) for f in os.listdir(fname) if os.path.isfile(os.path.join(fname, f))])
	else:
		parse_md([fname])
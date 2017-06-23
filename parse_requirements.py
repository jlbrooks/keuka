import markdown
import sys
import codecs
import os

class State:
	FIRST_NAME = 1
	DESCRIPTION = 2
	REQUIREMENTS = 3

# Setup Django, import relevant models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'local.settings')
import django
django.setup()
from badges.models import Badge
# Badge.objects.all().delete()

def first_char_index(line):
	for i,c in enumerate(line):
		if c.isalpha():
			return i
	return -1

def parse_md(fnames):
	for fname in fnames:
		with codecs.open(fname, mode='r', encoding='utf-8') as f:
			state = State.FIRST_NAME
			badge_title = ''
			badge_description = ''
			badge_reqs = ''
			# Process the file 1 line at a time
			for line in list(f):
				if state == State.FIRST_NAME:
					# Look for an h1
					if line[0:2] == '# ':
						badge_title = line[1:].strip()
						state = State.DESCRIPTION
				elif state == State.DESCRIPTION:
					# If we see an h2, we've gotten to requirements
					if line[0:3] == '## ':
						state = State.REQUIREMENTS
					# All other lines are description
					else:
						badge_description += line
				elif state == State.REQUIREMENTS:
					# If we see another h1, we're done with this badge
					if line[0:2] == '# ':
						cur_badge = Badge(
							title=badge_title,
							description=badge_description.strip(),
							requirements=badge_reqs.strip())
						cur_badge.save()

						# Reset description and requirements
						badge_description = ''
						badge_reqs = ''

						badge_title = line[1:].strip()
						state = State.DESCRIPTION
						continue
					# All other lines are requirements
					else:
						badge_reqs += line
			# Add the final badge
			cur_badge = Badge(
							title=badge_title,
							description=badge_description.strip(),
							requirements=badge_reqs.strip())
			cur_badge.save()


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
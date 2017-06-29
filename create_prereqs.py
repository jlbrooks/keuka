import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keuka.local_settings')
import django
django.setup()
from badges.models import Badge, BadgePrerequisite

# For one-off scripts, sometimes simpler is better ;-)
def sequence_number(title):
	title = title.lower()
	if len(title) < 3:
		return 0
	# There must be a space in the last 4 characters
	# This will filter out words that end with 'i' and 'iv'
	if title[-4:].find(' ') < 0:
		return 0
	if title[-2:] == 'iv':
		return 4
	if title[-3:] == 'iii':
		return 3
	if title[-2:] == 'ii':
		return 2
	if title[-1:] == 'i':
		return 1
	return 0

def strip_sequence(title):
	if sequence_number(title) == 0:
		return title
	return ' '.join(title.split(' ')[:-1])

def create_natural_prereqs(badges):
	for badge in badges:
		#print badge.title + ': ' + str(sequence_number(badge.title))
		seq = sequence_number(badge.title)
		if seq > 1:
			required_seq = seq - 1
			title_stripped = strip_sequence(badge.title)
			prev_badges = [b for b in badges 
							if strip_sequence(b.title) == title_stripped
							and sequence_number(b.title) == required_seq]
			if not prev_badges:
				print "Couldn't find pre-requisite for badge: " + badge.title
				continue
			prev_badge = prev_badges[0]
			#print '<--- ' + prev_badge.title
			prereq = BadgePrerequisite(badge=badge, required_badge=prev_badge)
			print 'Creating prereq for badge: ' + str(badge) + ': ' + str(prereq)


if __name__ == '__main__':
	badges = Badge.objects.all()

	create_natural_prereqs(badges)
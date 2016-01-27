import three_goals
import argparse


def get_championship(file_name):
	try:
		return three_goals.Championship.from_file("%s.db" % file_name)
	except Exception, e:
		print "Could not open championship file '%s.db'" % file_name
		raise e

def add_match(args):
	ch = get_championship(args.championship)
	ch.add_match(args.player, args.scored, args.conceded)
	return ch


default_championship_file = 'Championship'

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

add_match_parser = subparsers.add_parser('add-match')
add_match_parser.add_argument('player')
add_match_parser.add_argument('scored')
add_match_parser.add_argument('conceded')
add_match_parser.add_argument('--championship', default=default_championship_file)
add_match_parser.set_defaults(func=add_match)


args = parser.parse_args()
ch = args.func(args)
print "\n".join(three_goals.Tabella(ch, forBBCode = False).get_lines())


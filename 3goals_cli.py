import three_goals
import argparse
import time


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

def new_round(args):
	ch = get_championship(args.championship)
	ch.add_round(time.strftime('%Y-%m-%d'))
	return ch

def add_team(args):
	ch  = get_championship(args.championship)
	ch.add_team(args.player_name, args.team_name, args.character_id)
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

new_round_parser = subparsers.add_parser('new-round')
new_round_parser.add_argument('--championship', default=default_championship_file)
new_round_parser.set_defaults(func=new_round)

add_team_parser = subparsers.add_parser('add-team')
add_team_parser.add_argument('player_name')
add_team_parser.add_argument('team_name')
add_team_parser.add_argument('character_id')
add_team_parser.add_argument('--championship', default=default_championship_file)
add_team_parser.set_defaults(func=add_team)

args = parser.parse_args()
ch = args.func(args)
print "\n".join(three_goals.Tabella(ch, forBBCode = False).get_lines())


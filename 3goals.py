# -*- coding: utf-8 -*-

import operator
from collections import namedtuple
from recordtype import recordtype

Team = namedtuple('Team', ['player_name', 'team_name', 'character_id'])
Match = namedtuple('Match', ['player_name', 'scored', 'conceded'])
Result = recordtype('Result', ['player_name', ('wins', 0), ('losses', 0), ('draws', 0), ('scored', 0), ('conceded', 0)])

teams = None
rounds = None

with open("88.db", 'r') as f:
	s = eval(f.read().decode('utf-8'))
	teams = s['teams'];
	rounds = s['rounds']

team_lookup = { team.player_name: team for team in teams }
result_lookup = { team.player_name: Result(team.player_name) for team in teams }

for day, matches in rounds.iteritems():
	for match in matches:

		if match.player_name not in result_lookup:
			print "WARNING name not found %s" % match.player_name
			continue

		res = result_lookup[match.player_name]
		res.scored += match.scored
		res.conceded += match.conceded

		if match.scored > match.conceded:
			res.wins += 1
		elif match.scored < match.conceded:
			res.losses += 1
		else:
			res.draws += 1


def sort_result(x):
	return (
		x.wins*3 + x.draws*1,
		x.wins,
		x.scored - x.conceded,
		x.scored
	)

results = sorted(result_lookup.values(), key=lambda x: team_lookup[x.player_name].team_name, reverse=True);
results = sorted(results, key=sort_result)

#[charid=nnn name=sss]
namecollen = max([len(team.team_name) for team in teams]) + 2

padchar = '.'

def num_col(num):
	return str(num).rjust(3, padchar).ljust(4, padchar)

def get_row(idx, result, bbcode=False):
	team = team_lookup[result.player_name]

	name = team.team_name.ljust(namecollen, padchar)
	if bbcode:
		name = '[charid=%s name=%s]' % (team.character_id, name)

	pts = num_col(result.wins*3 + result.draws)
	wins = num_col(result.wins)
	draws = num_col(result.draws)
	losses = num_col(result.losses)

	gd = num_col(result.scored - result.conceded)
	sc = num_col(result.scored)
	cn = num_col(result.conceded)

	return (str(idx+1).rjust(2, padchar), name, pts, wins, draws, losses, gd, sc, cn)

print ".#|%s||%s||%s|%s|%s||%s||%s|%s" % ("Csapat".ljust(namecollen, padchar), num_col("Pts"), num_col("W"), num_col("D"), num_col("L"), num_col("GD"), num_col("Sc"), num_col("Cn"))
print "--+%s++----++----+----+----++----++----+----" % "-".ljust(namecollen, "-")
for idx, result in enumerate(reversed(results)):
	print ("%s|%s||%s||%s|%s|%s||%s||%s|%s" % get_row(idx, result, True))

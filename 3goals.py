# -*- coding: utf-8 -*-

import operator
from collections import namedtuple
from recordtype import recordtype

Team = namedtuple('Team', ['player_name', 'team_name', 'character_id'])
Match = namedtuple('Match', ['player_name', 'scored', 'conceded'])
Result = recordtype('Result', ['player_name', ('wins', 0), ('losses', 0), ('draws', 0), ('scored', 0), ('conceded', 0)])

def _result_sorter(x):
	return (
		x.wins*3 + x.draws*1,
		x.wins,
		x.scored - x.conceded,
		x.scored
	)


class Championship:
	def __init__(self, teams, rounds):
		self.teams = teams
		self.rounds = rounds

		self.team_lookup = { team.player_name: team for team in teams }
		self.result_lookup = { team.player_name: Result(team.player_name) for team in teams }

	@classmethod
	def from_file(cls, file_name):
		with open(file_name, 'r') as f:
			s = eval(f.read().decode('utf-8'))
			return cls(s['teams'], s['rounds'])

	@classmethod
	def load_default(cls):
		return Championship.from_file("Championship.db");

	def calc_results(self):
		for day, matches in self.rounds.iteritems():
			for match in matches:
				res = self.result_lookup[match.player_name]
				res.scored += match.scored
				res.conceded += match.conceded

				if match.scored > match.conceded:
					res.wins += 1
				elif match.scored < match.conceded:
					res.losses += 1
				else:
					res.draws += 1

	def get_sorted_results(self):
		results = sorted(self.result_lookup.values(), key=lambda x: self.team_lookup[x.player_name].team_name, reverse=True);
		results = sorted(results, key=_result_sorter)
		return results



padchar = '.'

def _num_col(num):
	return str(num).rjust(3, padchar).ljust(4, padchar)

def _get_row(idx, team, result, namecollen, bbcode=False):
	name = team.team_name.ljust(namecollen, padchar)
	if bbcode:
		name = '[charid=%s name=%s]' % (team.character_id, name)

	pts = _num_col(result.wins*3 + result.draws)
	wins = _num_col(result.wins)
	draws = _num_col(result.draws)
	losses = _num_col(result.losses)

	gd = _num_col(result.scored - result.conceded)
	sc = _num_col(result.scored)
	cn = _num_col(result.conceded)

	return (str(idx+1).rjust(2, padchar), name, pts, wins, draws, losses, gd, sc, cn)

def print_table(championship):
	results = championship.get_sorted_results()

	#[charid=nnn name=sss]
	namecollen = max([len(team.team_name) for team in ch.teams]) + 2


	print ".#|%s||%s||%s|%s|%s||%s||%s|%s" % ("Csapat".ljust(namecollen, padchar), _num_col("Pts"), _num_col("W"), _num_col("D"), _num_col("L"), _num_col("GD"), _num_col("Sc"), _num_col("Cn"))
	print "--+%s++----++----+----+----++----++----+----" % "-".ljust(namecollen, "-")
	for idx, result in enumerate(reversed(results)):
		print ("%s|%s||%s||%s|%s|%s||%s||%s|%s" % _get_row(idx, ch.team_lookup[result.player_name], result, namecollen, True))


if __name__ == '__main__':
	ch = Championship.load_default()
	ch.calc_results()
	print_table(ch)

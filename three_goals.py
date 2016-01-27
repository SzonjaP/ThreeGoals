# -*- coding: utf-8 -*-

import operator
from collections import namedtuple


Team = namedtuple('Team', ['player_name', 'team_name', 'character_id'])
Match = namedtuple('Match', ['player_name', 'scored', 'conceded'])
Result = namedtuple('Result', ['player_name', 'wins', 'losses', 'draws', 'scored', 'conceded'])

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
		self._calc_results();

	@classmethod
	def from_file(cls, file_name):
		with open(file_name, 'r') as f:
			s = eval(f.read().decode('utf-8'))
			return cls(s['teams'], s['rounds'])

	def _calc_results(self):
		res = {}
		player_matches = { team.player_name: [] for team in self.teams }

		for day, matches in self.rounds.iteritems():
			for match in matches:
				player_matches[match.player_name].append(match);

		for player_name, matches in player_matches.iteritems():
			scored = 0;
			conceded = 0;
			wins = 0;
			losses = 0;
			draws = 0;
			for match in matches:
				scored += match.scored
				conceded += match.conceded

				if match.scored > match.conceded:
					wins += 1
				elif match.scored < match.conceded:
					losses += 1
				else:
					draws += 1

				res[player_name] = Result(player_name, wins, losses, draws, scored, conceded);

		self.result_lookup = res

	def add_match(self, player_name, scored, conceded):
		if not player_name in self.team_lookup:
			raise Exception("No registered team for %s" % player_name)
		for match in self.last_round:
			if match.player_name == player_name:
				raise Exception("Player %s already has a match registered for the current round" % player_name)

		self.last_round.append(Match(player_name, int(scored), int(conceded)))
		self._calc_results()


	@property
	def last_round(self):
		return self.rounds[sorted(self.rounds)[-1]]

	def get_sorted_results(self, sorter = _result_sorter):
		results = sorted(self.result_lookup.values(), key=lambda x: self.team_lookup[x.player_name].team_name, reverse=True);
		results = sorted(results, key=sorter)
		return results



class Tabella:
	def __init__(self, championship, padchar = '.', forBBCode = True):
		self.padchar = padchar
		self.forBBCode = forBBCode
		self.championship = championship

	def _num_col(self, num):
		return str(num).rjust(3, self.padchar).ljust(4, self.padchar)

	def _get_row(self, idx, team, result, namecollen):
		name = team.team_name.ljust(namecollen, self.padchar)
		if self.forBBCode:
			name = '[charid=%s name=%s]' % (team.character_id, name)

		pts = self._num_col(result.wins*3 + result.draws)
		wins = self._num_col(result.wins)
		draws = self._num_col(result.draws)
		losses = self._num_col(result.losses)

		gd = self._num_col(result.scored - result.conceded)
		sc = self._num_col(result.scored)
		cn = self._num_col(result.conceded)

		return (str(idx+1).rjust(2, self.padchar), name, pts, wins, draws, losses, gd, sc, cn)

	def get_lines(self, sorter = _result_sorter):
		results = self.championship.get_sorted_results(sorter)
		namecollen = max([len(team.team_name) for team in self.championship.teams]) + 2

		lines = []
		lines.append(
			".#|%s||%s||%s|%s|%s||%s||%s|%s" % (
				"Csapat".ljust(namecollen, self.padchar),
				self._num_col("Pts"),
				self._num_col("W"),
				self._num_col("D"),
				self._num_col("L"),
				self._num_col("GD"),
				self._num_col("Sc"),
				self._num_col("Cn"))
		)
		lines.append("--+%s++----++----+----+----++----++----+----" % "-".ljust(namecollen, "-"))
		for idx, result in enumerate(reversed(results)):
			lines.append("%s|%s||%s||%s|%s|%s||%s||%s|%s" % self._get_row(idx, self.championship.team_lookup[result.player_name], result, namecollen))

		return lines


if __name__ == '__main__':
	ch = Championship.from_file("Championship.db")
	table = Tabella(ch)
	print "\n".join(table.get_lines())

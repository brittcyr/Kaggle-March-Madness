#!usr/bin/python
from reader import read_data
import numpy as np

K = 20.0

def elo_scores_tourney(regular_season_results = None, tourney_results = None, seeds = None):
    if regular_season_results is None:
        regular_season_results, tourney_results, seeds = read_data()

    teams = set([x[2] for x in regular_season_results])
    elo_scores_by_season = {}
    games = []
    seasons = list(set([x[0] for x in regular_season_results]))
    for season in seasons:
        tourney_teams = []
        for TSeason,Team in seeds:
            if TSeason == season:
                tourney_teams.append(Team)

        elo_scores = {}
        for team in tourney_teams:
            elo_scores[team] = 1500
        for Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf in regular_season_results:
            if Season != season: continue
            if Wteam not in tourney_teams or Lteam not in tourney_teams: continue

            # All the games are for the current season
            margin_of_victory = int(Wscore) - int(Lscore) if int(Numot) == 0 else 0
            numerator = (margin_of_victory + 3)**.8
            denominator = (elo_scores[Wteam] - elo_scores[Lteam]) * .006 + 7.5

            rating_change = K * numerator / denominator
            elo_scores[Wteam] = elo_scores[Wteam] + rating_change
            elo_scores[Lteam] = elo_scores[Lteam] - rating_change

        elo_scores_by_season[season] = elo_scores

    # 1.0 / (10**(- elo_diff /400.0) + 1)
    return elo_scores_by_season

if __name__ == '__main__':
    print elo_scores_tourney()

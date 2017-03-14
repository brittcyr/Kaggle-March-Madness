#!usr/bin/python
from reader import read_data
import numpy as np

SAMPLES = 1000

def points_model(regular_season_results = None, tourney_results = None, seeds = None):
    if regular_season_results is None:
        regular_season_results, tourney_results, seeds = read_data()

    teams = set([x[2] for x in regular_season_results])

    # The idea of this model is to take the points scored in each game vs average
    # Uses a Monte Carlo method to take from your points distribution for

    seasons = list(set([x[0] for x in regular_season_results]))
    points_distributions = {}
    for season in seasons:
        points_for = {}
        points_against = {}
        for team in teams:
            points_for[team] = []
            points_against[team] = []
        for Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf in regular_season_results:
            if Season != season: continue

            Wscore = int(Wscore)
            Lscore = int(Lscore)

            points_for[Wteam].append(Wscore)
            points_for[Lteam].append(Lscore)
            points_against[Wteam].append(Lscore)
            points_against[Lteam].append(Wscore)

        for team in teams:
            if len(points_for[team]) == 0: continue
            for_mu = np.mean(np.array(points_for[team]))
            for_std = np.std(np.array(points_for[team]))

            against_mu = np.mean(np.array(points_against[team]))
            against_std = np.std(np.array(points_against[team]))

            points_distributions[(season,team)] = (for_mu, for_std, against_mu, against_std)

    return points_distributions


def points_prob(points_distributions,Season,team1,team2):
    wins1 = 0
    wins2 = 0
    (for_mu1, for_std1, against_mu1, against_std1) = points_distributions[(Season,team1)]
    (for_mu2, for_std2, against_mu2, against_std2) = points_distributions[(Season,team2)]
    # Formula for getting a random point from the distribution
    scores_for1 = np.random.normal(for_mu1, for_std1, SAMPLES)
    scores_for2 = np.random.normal(for_mu2, for_std2, SAMPLES)
    scores_against1 = np.random.normal(against_mu1, against_std1, SAMPLES)
    scores_against2 = np.random.normal(against_mu2, against_std2, SAMPLES)
    for i in xrange(SAMPLES):
        if scores_for1[i] > scores_for2[i]:
            wins1 += 1
        else:
            wins2 += 1

        if scores_against1[i] > scores_against2[i]:
            wins2 += 1
        else:
            wins1 += 1

    return float(wins1) / (SAMPLES * 2)

if __name__ == '__main__':
    print points_model()

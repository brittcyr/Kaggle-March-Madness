#!usr/bin/python
import sys
from neural_net import train, test, make_neural_net, evaluate
from random import shuffle
from reader import read_data, get_tourney_teams
from seeds_model import seeds_historic, seed_prob
from elo import elo_scores, elo_prob
from elo_late import elo_scores_late
from elo_tourney import elo_scores_tourney
from points_model import points_model, points_prob

MAX_ITERATIONS = 10000


def construct_data():
    regular_season_results, tourney_results, seeds = read_data()
    results, inter_regions = seeds_historic(regular_season_results, tourney_results, seeds)
    elo_scores_by_season = elo_scores(regular_season_results, tourney_results, seeds)
    elo_scores_by_season_late = elo_scores_late(regular_season_results, tourney_results, seeds)
    elo_scores_by_season_tourney = elo_scores_tourney(regular_season_results, tourney_results, seeds)
    points_distributions = points_model(regular_season_results, tourney_results, seeds)

    DATA = []
    for row in tourney_results:
        [Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3, \
                Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga, \
                Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf] = row
        SEED_SCORE = seed_prob(seeds,Season,Wteam,Lteam,results,inter_regions)
        POINTS_SCORE = points_prob(points_distributions,Season,Wteam,Lteam)
        ELO_SCORE = elo_prob(Season,Wteam,Lteam,elo_scores_by_season)
        ELO_LATE_SCORE = elo_prob(Season,Wteam,Lteam,elo_scores_by_season_late)
        ELO_TOURNEY_SCORE = elo_prob(Season,Wteam,Lteam,elo_scores_by_season_tourney)
        data = (SEED_SCORE, POINTS_SCORE, ELO_SCORE, ELO_LATE_SCORE, ELO_TOURNEY_SCORE, 1.0)
        DATA.append(data)
        reversed_data = tuple([1.0 - x for x in data])
        DATA.append(reversed_data)
    return DATA

def construct_target_data():
    regular_season_results, tourney_results, seeds = read_data()
    results, inter_regions = seeds_historic(regular_season_results, tourney_results, seeds)
    elo_scores_by_season = elo_scores(regular_season_results, tourney_results, seeds)
    elo_scores_by_season_late = elo_scores_late(regular_season_results, tourney_results, seeds)
    elo_scores_by_season_tourney = elo_scores_tourney(regular_season_results, tourney_results, seeds)
    points_distributions = points_model(regular_season_results, tourney_results, seeds)
    tourney_teams = get_tourney_teams()

    DATA = []
    Season = '2017'
    for t1 in tourney_teams:
        for t2 in tourney_teams:
            if t1 >= t2:
                continue
            SEED_SCORE = seed_prob(seeds,Season,t1,t2,results,inter_regions)
            POINTS_SCORE = points_prob(points_distributions,Season,t1,t2)
            ELO_SCORE = elo_prob(Season,t1,t2,elo_scores_by_season)
            ELO_LATE_SCORE = elo_prob(Season,t1,t2,elo_scores_by_season_late)
            ELO_TOURNEY_SCORE = elo_prob(Season,t1,t2,elo_scores_by_season_tourney)
            data = (SEED_SCORE, POINTS_SCORE, ELO_SCORE, ELO_LATE_SCORE, ELO_TOURNEY_SCORE, t1, t2)
            DATA.append(data)
    return DATA


def main(max_iterations=MAX_ITERATIONS):
    verbose = False
    data = construct_data()
    print "Got data ", len(data), "rows"
    neural_net_func = make_neural_net

    print "-"*40
    print "Training on data"
    nn = neural_net_func()

    data_len = len(data)
    cutoff = int(data_len * .8)

    for i in xrange(max_iterations):
        shuffle(data)
        training_data = data[:cutoff]
        test_data = data[cutoff:]

        train(nn, training_data, max_iterations=1, verbose=verbose, rate=.01)
        if i % 100 == 0:
            print "Trained weights:"
            for w in nn.weights:
                print "Weight '%s': %f"%(w.get_name(),w.get_value())

            print "Testing on %s test-data" %(i)
            result = test(nn, test_data, verbose=verbose)
            print "Accuracy: %f"%(result)

    target_data = construct_target_data()
    results = evaluate(nn, target_data, False)

    f = open('results.csv', 'w')
    f2 = open('results2.csv', 'w')
    s = "id,pred\n"
    f.write(s)
    f2.write(s)
    for i in xrange(len(results)):
        data = target_data[i]
        result = results[i]
        updated_data = list(data)[:5]
        t1 = data[5]
        t2 = data[6]
        if result > max(updated_data) or result > max(updated_data):
            result = max(updated_data) if max(updated_data) < .99 else .99
        if result < min(updated_data) or result < min(updated_data):
            result = min(updated_data) if min(updated_data) > .01 else .01
        s = "2017_%s_%s,%f\n" % (t1, t2, result)
        f.write(s)

        (SEED_SCORE, POINTS_SCORE, ELO_SCORE, ELO_LATE_SCORE, ELO_TOURNEY_SCORE, t1, t2) = data
        result2 = (SEED_SCORE * 7 + POINTS_SCORE * 2 + ELO_SCORE * 6 + \
                ELO_LATE_SCORE + ELO_TOURNEY_SCORE * 4) / 20.0
        s2 = "2017_%s_%s,%f\n" % (t1, t2, result2)
        f2.write(s2)

    f.close()
    f2.close()

if __name__ == '__main__':
    main()

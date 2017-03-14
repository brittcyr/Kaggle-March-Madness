#!usr/bin/python
from reader import read_data


def seeds_historic(regular_season_results = None, tourney_results = None, seeds = None):
    if regular_season_results is None:
        regular_season_results, tourney_results, seeds = read_data()

    results = {}
    for i in range(1, 17):
        for j in range(1, 17):
            results[(i, j)] = 0

    inter_regions = {}

    for x in tourney_results:
        [Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf] = x
        win_seed = seeds[(Season,Wteam)]
        lose_seed = seeds[(Season,Lteam)]

        regions = tuple([win_seed[0], lose_seed[0]])
        if regions[0] != regions[1]:
            if regions in inter_regions:
                inter_regions[regions] = inter_regions[regions] + 1
            else:
                inter_regions[regions] = 1

            regions_rev = tuple([lose_seed[0], win_seed[0]])
            if regions_rev not in inter_regions:
                inter_regions[regions_rev] = 0


        if len(win_seed) == 4:
            win_seed = win_seed[:-1]
        if len(lose_seed) == 4:
            lose_seed = lose_seed[:-1]

        seed_nums = tuple([int(x) for x in [win_seed[1:], lose_seed[1:]]])
        if seed_nums in results:
            results[seed_nums] = results[seed_nums] + 1

    return results, inter_regions


def seed_prob(seeds,Season,Team1,Team2,results,inter_regions):
    seed1 = seeds[(Season,Team1)]
    seed2 = seeds[(Season,Team2)]
    if len(seed1) == 4:
        seed1 = seed1[:-1]
    if len(seed2) == 4:
        seed2 = seed2[:-1]
    region1 = seed1[0]
    region2 = seed2[0]

    seed_nums_wins = tuple([int(x) for x in [seed1[1:], seed2[1:]]])
    seed_nums_loss = tuple([int(x) for x in [seed2[1:], seed1[1:]]])

    # For inter-regional games, don't use seeds.
    if region1 != region2:
        return float(inter_regions[(region1, region2)]) / \
                (inter_regions[(region1, region2)] + inter_regions[(region2, region1)])
    if results[seed_nums_loss] + results[seed_nums_wins] == 0:
        return .5
    return float(results[seed_nums_wins]) / (results[seed_nums_loss] + results[seed_nums_wins])

if __name__ == '__main__':
    print seeds_historic()

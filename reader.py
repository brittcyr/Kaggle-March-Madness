#!usr/bin/python


def read_data():
    regular_season_results = []
    f = open('2016/RegularSeasonDetailedResults.csv', 'r')
    f.readline()
    for line in f:
        row = line.strip()
        [Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf] = row.split(',')
        regular_season_results.append(row.split(','))


    tourney_results = []
    f = open('TourneyDetailedResults.csv', 'r')
    f.readline()
    for line in f:
        row = line.strip()
        [Season,Daynum,Wteam,Wscore,Lteam,Lscore,Wloc,Numot,Wfgm,Wfga,Wfgm3,Wfga3,Wftm,Wfta,Wor,Wdr,Wast,Wto,Wstl,Wblk,Wpf,Lfgm,Lfga,Lfgm3,Lfga3,Lftm,Lfta,Lor,Ldr,Last,Lto,Lstl,Lblk,Lpf] = row.split(',')
        tourney_results.append(row.split(','))

    seeds = {}
    f = open('2016/TourneySeeds.csv', 'r')
    f.readline()
    for line in f:
        row = line.strip()
        [Season,Seed,Team] = row.split(',')
        seeds[(Season, Team)] = Seed


    return regular_season_results, tourney_results, seeds

def get_tourney_teams(season='2016'):
    teams = []
    f = open('2016/TourneySeeds.csv', 'r')
    f.readline()
    for line in f:
        row = line.strip()
        [Season,Seed,Team] = row.split(',')
        if Season == season:
            teams.append(Team)

    return teams

if __name__ == '__main__':
    regular_season_results, tourney_results, seeds = read_data()

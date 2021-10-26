''' Convert.py
    By Zack Johnson October 12, 2021

    Converts Olympics data from the kaggle olympics database into seperate CSV files
    suited for use in a psql database.
    Data from:
    https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results
    Note: NULL data is denoted 'NA'
    Note: Inefficent implementation, takes several minutes (<30) to run.
'''

import csv
import sys

# Column nnumbers in the athlete_events.csv file
OLYMPIAN_NAME = 1
OLYMPIAN_SEX = 2
OLYMPIAN_AGE = 3
OLYMPIAN_TEAM = 6
OLYMPIAN_NOC = 7
OLYMPIAN_YEAR = 9
OLYMPIAN_SEASON = 10
OLYMPIAN_CITY = 11
OLYMPIAN_SPORT = 12
OLYMPIAN_EVENT = 13
OLYMPIAN_MEDAL = 14


class Athlete:
    def __init__(self, name, sex, birth_year):
        self.id  = None
        self.name = name
        self.sex = sex
        self.birth_year = birth_year

    def get_id(self):
        return self.id

    def __eq__(self, other):
        '''makeing the simplifying assumption that no two athletes have the same name'''
        return self.name == other.name

    def list_format(self):
        return [self.id, self.name, self.sex, self.birth_year]

class Games:
    def __init__(self, year, season, city):
        self.year = year
        self.city = city
        self.season = season

    def get_id(self):
        return self.year

    def __eq__(self, other):
        '''since no two games happen in the same year'''
        return self.year == other.year

    def list_format(self):
        return [self.year, self.season, self.city]

class Event:
    def __init__(self, event, sport):
        self.id = None
        self.event = event
        self.sport = sport

    def get_id(self):
        return self.id

    def __eq__(self, other):
        return self.event == other.event

    def list_format(self):
        return [self.id, self.event, self.sport]

class Result:
    def __init__(self, game_year, event_id, athlete_id, noc_abbr, result):
        self.game_year = game_year
        self.event_id = event_id
        self.athlete_id = athlete_id
        self.noc_abbr = noc_abbr
        self.result = result

    def list_format(self):
        return [self.game_year, self.event_id, self.athlete_id, self.noc_abbr, self.result]

class NOC:
    def __init__(self, abbr, name):
        self.abbreviation = abbr
        self.name = name

    def get_id(self):
        return self.abbreviation

    def __eq__(self, other):
        '''assuming abbreviations were never re-used'''
        return self.abbreviation == other.abbreviation

    def list_format(self):
        return [self.abbreviation, self.name]

class OlympicsDataSource:
    def __init__(self, csv_file):
        self.athlete_list = []
        self.games_list = []
        self.events_list = []
        self.noc_list = []
        self.results_list = []

        with open(csv_file, 'r') as athlete_events_csv:
            reader = csv.reader(athlete_events_csv)
            next(reader)
            for row in reader:
                athlete = self.add_athlete(row[OLYMPIAN_NAME], row[OLYMPIAN_SEX], row[OLYMPIAN_AGE], row[OLYMPIAN_YEAR])
                games = self.add_games(row[OLYMPIAN_YEAR], row[OLYMPIAN_SEASON], row[OLYMPIAN_CITY])
                event = self.add_event(row[OLYMPIAN_EVENT], row[OLYMPIAN_SPORT])
                noc = self.add_noc(row[OLYMPIAN_NOC], row[OLYMPIAN_TEAM])
                result = Result(games.get_id(), event.get_id(), athlete.get_id(), noc.get_id(), row[OLYMPIAN_MEDAL])
                self.results_list.append(result)

    def add_noc(self, abbr, name):
        new_noc = NOC(abbr, name)
        for noc in self.noc_list:
            if(noc == new_noc):
                return noc
        self.noc_list.append(new_noc)
        return new_noc

    def add_event(self, event, sport):
        new_event = Event(event, sport)
        for event in self.events_list:
            if(event == new_event):
                return event
        new_event.id = len(self.events_list)
        self.events_list.append(new_event)
        return new_event

    def add_games(self, year, season, city):
        new_games = Games(year, season, city)
        for games in self.games_list:
            if(games == new_games):
                return games
        self.games_list.append(new_games)
        return new_games

    def add_athlete(self, name, sex, age, year):
        try:
            birth_year = int(year) - int(age) - 1 #games are often early in the year
        except:
            birth_year = "NA" # NULL is NA elsewhere in the dataset,

        new_athlete = Athlete(name, sex, birth_year)
        for athlete in self.athlete_list:
            if(athlete == new_athlete):
                return athlete
        new_athlete.id = len(self.athlete_list)
        self.athlete_list.append(new_athlete)
        return new_athlete


def main():
    data_source = OlympicsDataSource('athlete_events.csv')

    print('number of athletes:', len(data_source.athlete_list))
    print('number of games:', len(data_source.games_list))
    print('number of NOCs:', len(data_source.noc_list))

    with open('athletes.csv','w') as athletes_csv:
        writer = csv.writer(athletes_csv)
        for athlete in data_source.athlete_list:
            writer.writerow(athlete.list_format())

    with open('games.csv', 'w') as games_csv:
        writer = csv.writer(games_csv)
        for games in data_source.games_list:
            writer.writerow(games.list_format())

    with open('events.csv','w') as events_csv:
        writer = csv.writer(events_csv)
        for events in data_source.events_list:
            writer.writerow(events.list_format())

    with open('noc.csv','w') as noc_csv:
        writer = csv.writer(noc_csv)
        for noc in data_source.noc_list:
            writer.writerow(noc.list_format())

    with open('results.csv','w') as results_csv:
        writer = csv.writer(results_csv)
        for result in data_source.results_list:
            writer.writerow(result.list_format())

if __name__ == '__main__':
    main()

''' olympics.py
    By: Zack Johnson October 17, 2021

    A command line interface to access the olympics.sql database.
    Use: python3 olympics.py --help for more information.
'''

import argparse
import psycopg2

from config import password
from config import database
from config import user

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--athletes', metavar='<keyword>', help= """Prints a list of athletes who's
        name contains <keyword> and a list of all of their medal winning events
        sorted by year.""")
group.add_argument('-n', '--noc', '--nation', metavar='<noc_id>', nargs='?', const='all', help="""List athletes that have
        competed for the National Olympic Committee (NOC) denoted by <noc_id>.
        OR: use 'all' to list all NOCs sorted by their all time gold medal total.""")

def query_noc_golds(cursor):
    query = '''SELECT count(result) AS Golds, nocs.abbreviation, nocs.name
            FROM nocs, results
            WHERE nocs.abbreviation = results.noc_abbr
            AND LOWER(result) = 'gold'
            GROUP BY nocs.abbreviation, nocs.name
            ORDER BY Golds DESC;'''
    cursor.execute(query)

def query_noc_members(cursor, noc):
    query = '''SELECT DISTINCT athletes.name, sex, birth_year
            FROM athletes, nocs, results
            WHERE athletes.id = results.athlete_id
            AND nocs.abbreviation = results.noc_abbr
            AND nocs.abbreviation = %s;'''
    cursor.execute(query, (noc.upper(), ))

def query_athlete(cursor, athlete):
    query = '''SELECT result, events.name AS event, games.year, games.city
            FROM athletes, games, results, nocs, events
            WHERE athletes.id = results.athlete_id
            AND games.year = results.games_year
            AND nocs.abbreviation = results.noc_abbr
            AND events.id = results.event_id
            AND result IS NOT NULL
            AND LOWER(athletes.name) LIKE %s
            ORDER BY games.year;'''
    cursor.execute(query, ('%' + athlete.lower() + '%',))

def main():
    args = parser.parse_args()
    # Connect to the database
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    cursor = connection.cursor()
    try:
        if args.noc is not None:
            if args.noc == 'all':
                query_noc_golds(cursor)
                print('===== NOCs by All Time Gold Medals =====')
                for row in cursor:
                    print(row[0], '  |  ', row[1], '  |  ', row[2])
            else:
                query_noc_members(cursor, args.noc)
                print(f'===== Athletes who play for {args.noc.upper()} =====')
                print('Name         Sex    Birth Year')
                for row in cursor:
                    print(row[0], '    ', row[1], '    ', row[2])

        if args.athletes is not None:
            query_athlete(cursor, args.athletes)
            print(f'===== Medals Won by {args.athletes} =====')
            print()
            for row in cursor:
                print(row[0], '    ', row[1], '    ', row[2], row[3])

    except Exception as e:
        print(e)
        exit()

    connection.close()

if __name__ == '__main__':
    main()

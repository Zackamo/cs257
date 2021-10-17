''' olympics.py
    By: Zack Johnson October 17, 2021

    A command line interface to access the olympics.sql database.
'''

import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-a', '--athletes', metavar='<keyword>', help= """Prints a list of athletes who's
        name contains <keyword> and a list of all of their medal winning events
        sorted by year.""")
group.add_argument('-n', '--noc', '--nation', metavar='<noc_id>', help="""List athletes that have
        competed for the National Olympic Committee (NOC) denoted by <noc_id>.
        If missing or invalid, instead list all NOCs sorted by their all time
        gold medal total.""")


def main():
    args = parser.parse_args()


if __name__ == '__main__':
    main()

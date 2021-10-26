#!/usr/bin/env python3
'''
    olympics-api.py
    Zack Johnson, 25 October, 2021

    A Flask API for the Olympics dataset.
'''
import sys
import argparse
import flask
import json
import psycopg2

from config import password
from config import database
from config import user

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

@app.route('/games')
def get_games():
    '''Returns a list of dictionaries, each containing an olympic games'''
    games_list = []
    connection, cursor = get_database()
    query = '''SELECT * FROM games'''
    cursor.execute(query)
    for row in cursor: #YEAR, SEASON, CITY
        olympic_game = {"year":row[0], "season":row[1], "city":row[2]}
        games_list.append(olympic_game)
    connection.close()
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    '''Returns a list of dictionaries, each containing a noc: name and abbreviation'''
    nocs_list = []
    connection, cursor = get_database()
    query = '''SELECT * FROM nocs'''
    cursor.execute(query)
    for row in cursor: #ABBREVIATION, YEAR
        noc = {'abbr':row[0], 'year':row[1]}
        nocs_list.append(noc)
    connection.close()
    return json.dumps(nocs_list)

@app.route('/medalists/games/<games_year>')
def get_games_results(games_year):
    ''' Returns a list of dictionaries, each containing an event and the athlete that won it
        Note: my database id's Olympic games by their year.
    '''
    events_list = []
    noc = flask.request.args.get('noc')
    connection, cursor = get_database()
    query = ''' SELECT athletes.id, athletes.name, athletes.sex, events.sport, events.name, results.result
                FROM athletes, events, results
                WHERE athletes.id = results.athlete_id
                AND results.noc_abbr LIKE %s
                AND results.games_year = %s
                AND results.result IS NOT NULL;'''
    cursor.execute(query, ('%' + noc + '%', games_year))
    for row in cursor:
        event = {'athlete_id':row[0], 'athlete_name':row[1], 'athlete_sex':row[2], 'sport':row[3], 'event':row[4], 'medal':row[5]}
        events_list.append(event)

    connection.close()
    return json.dumps(events_list)

@app.route('/actor/<last_name>')
def get_actor(last_name):
    ''' Returns the first matching actor, or an empty dictionary if there's no match. '''
    actor_dictionary = {}
    lower_last_name = last_name.lower()
    for actor in actors:
        if actor['last_name'].lower().startswith(lower_last_name):
            actor_dictionary = actor
            break
    return json.dumps(actor_dictionary)

@app.route('/movies')
def get_movies():
    ''' Returns the list of movies that match GET parameters:
          start_year, int: reject any movie released earlier than this year
          end_year, int: reject any movie released later than this year
          genre: reject any movie whose genre does not match this genre exactly
        If a GET parameter is absent, then any movie is treated as though
        it meets the corresponding constraint. (That is, accept a movie unless
        it is explicitly rejected by a GET parameter.)
    '''
    movie_list = []
    genre = flask.request.args.get('genre')
    start_year = flask.request.args.get('start_year', default=0, type=int)
    end_year = flask.request.args.get('end_year', default=10000, type=int)
    for movie in movies:
        if genre is not None and genre != movie['genre']:
            continue
        if movie['year'] < start_year:
            continue
        if movie['year'] > end_year:
            continue
        movie_list.append(movie)

    return json.dumps(movie_list)

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

def get_database():
    ''' Establishes a connection to the olympics database
        RETURN: the connection and a cursor object '''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    return connection, connection.cursor()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)

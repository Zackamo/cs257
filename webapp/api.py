'''
    api.py
    for the lego webapp project
    Zack Johnson and Amir Al-Sheikh, 9 November 2021

    Flask API to support the lego web application.
    Based on a template by Jeff Ondich
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/minifigs/')
def get_authors():

    query = '''SELECT minifigs.name, minifigs.fig_num, sets.name
               FROM minifigs, sets, inventories, inventory_minifigs
               WHERE minifigs.fig_num = inventory_minifigs.fig_num
               AND inventory_minifigs.inventory_id = inventories.id
               AND inventories.set_num = sets.set_num
               LIMIT 15;'''

    minifig_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            minifig = {'name':row[0],
                      'fig_num':row[1],
                      'set_name':row[2]}
            minifig_list.append(minifig)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(minifig_list)

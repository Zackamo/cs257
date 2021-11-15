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

@api.route('/sets/')
def get_sets():
    ''' Returns a list of LEGO sets in json form corresponding to the GET arguments
            search_for, str: only find sets with names LIKE %search_string%
            theme, str: only return sets with theme names LIKE %theme%
            sort_by, str: sets the psql column to sort by
            order, str: 'asc' or 'desc' the latter adds the DESC command
        if GET parameters are absent, return an arbitrary subset of the list of sets
    '''
    search_string = flask.request.args.get('search_for', default='').lower()
    theme = flask.request.args.get('theme', default='')
    sort_by = flask.request.args.get('sort_by', default='')
    order = flask.request.args.get('order', default='asc')

    query = '''SELECT sets.set_num, sets.name, themes.name, sets.num_parts, SUM(inventory_minifigs.quantity) AS num_figs, sets.year
            FROM sets, themes, inventories, inventory_minifigs
            WHERE sets.theme_id = themes.id
            AND sets.set_num = inventories.set_num
            AND inventory_minifigs.inventory_id = inventories.id
            AND LOWER(sets.name) LIKE %s
            '''
    input_tuple = ('%' + search_string + '%',)
    if (theme != ''):
        input_tuple += (theme,)
        query += ' AND sets.theme_id = %s '
    query += ' GROUP BY sets.set_num, sets.name, themes.name, sets.num_parts, sets.year '

    set_headers = ['sets.set_num', 'sets.name', 'themes.name', 'sets.num_parts', 'num_figs', 'sets.year']
    try:
        sort_by = int(sort_by)
    except:
        sort_by = -1
    order_by_string = ''
    if (sort_by >= 0 and sort_by < len(set_headers)):
        order_by_string = ' ORDER BY ' + set_headers[sort_by]
        if (order == 'desc'):
            order_by_string += ' DESC '
    query += order_by_string
    query += '''
    LIMIT 100;'''

    sets_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print(input_tuple)
        cursor.execute(query, input_tuple)
        for row in cursor:
            set = {'set_num':row[0],
                      'name':row[1],
                      'theme':row[2],
                      'num_parts':row[3],
                      'num_figs':row[4],
                      'year':row[5]}
            sets_list.append(set)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(sets_list)

@api.route('/minifigs/')
def get_minifigs():

    search_string = flask.request.args.get('search_for', default='').lower()
    sort_by = flask.request.args.get('sort_by', default="-1")
    order = flask.request.args.get('order', default='asc')

    query = '''SELECT minifigs.fig_num, minifigs.name, minifigs.num_parts, COUNT(DISTINCT sets.name) AS sets_in
            FROM minifigs, sets, inventories, inventory_minifigs, themes
            WHERE minifigs.fig_num = inventory_minifigs.fig_num
            AND inventory_minifigs.inventory_id = inventories.id
            AND inventories.set_num = sets.set_num
            AND LOWER(minifigs.name) LIKE %s
            GROUP BY minifigs.fig_num, minifigs.name, minifigs.num_parts'''
    order_by_string = ''
    fig_headers = ['minifigs.fig_num', 'minifigs.name', 'minifigs.num_parts', 'sets_in']
    try:
        sort_by = int(sort_by)
    except:
        sort_by = -1
    if (sort_by >= 0 and sort_by < len(fig_headers)):
        order_by_string = ' ORDER BY '
        order_by_string += fig_headers[sort_by]
        if (order == 'desc'):
            order_by_string += ' DESC '
    query += order_by_string
    query += ''' LIMIT 100;'''

    minifig_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, ('%'+ search_string +'%',))
        for row in cursor:
            minifig = {'name':row[0],
                      'fig_num':row[1],
                      'num_parts':row[2],
                      'num_sets':row[3]}
            minifig_list.append(minifig)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(minifig_list)

@api.route('/help/')
def get_help():
    help_text = open('templates/help.txt').read()
    return flask.Response(help_text, mimetype='text/plain')

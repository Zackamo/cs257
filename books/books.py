'''
    books.py
    Zack Johnson and Alia Babinet, September 30, 2021

    Searches the books data set using BooksDataSource.
'''
import booksdatasource
import sys

authorFlags = ['-a','--search-author']
bookFlags = ['-t','--search-title']
yearsFlags = ['-y','--search-year']
helpFlags = ['-h','-?','--help']

def parseCommandLine():
    ''' Checks command syntax and routes to appropriate routine
    '''
    if (sys.argv[1] in helpFlags or len(sys.argv) <= 1):
        getHelp()
    elif (sys.argv[1] in authorFlags):
        if (len(sys.argv <= 3)):
            displayAuthors()
        else:
            statement = f'Usage: {sys.argv[0]} -a search_string \n'
            statement += 'searches and prints all authors in booksdatasource whose surname or given name contain search_string. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
    elif (sys.argv[1] in bookFlags):
        if (len(sys.argv) <= 4):
            displayBooks()
        else:
            statement = f'Usage: {sys.argv[0]} -t search_string [title | year] \n'
            statement += 'searches and prints all books in booksdatasource whose title contains search_string. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
    elif (sys.argv[1] in yearFlags):
        if (len(sys.argv <= 4)):
            displayYears()
        else:
            statement = f'Usage: {sys.argv[0]} -y start_year end_year \n'
            statement += '    searches and prints all books in booksdatasource published in or between start_year and end_year. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'

def displayAuthors():
    results = dataSource.authors(sys.argv[2])
    if (results[0] == 1):
        reportError(results[1])


def displayBooks():
    results = dataSource.books(sys.argv[2])
    if (results[0] == 1):
        reportError(results[1])

def displayYears():
    results = dataSource.books_between_years(sys.argv[2])
    if (results[0] == 1):
        reportError(results[1])

def reportError(message):


def getHelp():
    f = open('usage.txt', 'r')
    usageStatement = f.read()
    print(usageStatement)
    f.close()
    sys.exit()

def main():
    dataSource = booksdatasource('books1.csv')


if __name__ == '__main__':
    main()

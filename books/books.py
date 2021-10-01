'''
    books.py
    Zack Johnson and Alia Babinet, September 30, 2021

    Searches the books data set using BooksDataSource.
'''
import booksdatasource
import sys

authorFlags = ['-a','--search-author']
bookFlags = ['-t','--search-title']
yearFlags = ['-y','--search-year']
helpFlags = ['-h','-?','--help']

def parseCommandLine(dataSource):
    ''' Checks command syntax and routes to appropriate routine
    '''
    if (sys.argv[1] in helpFlags or len(sys.argv) <= 1):
        getHelp()
    elif (sys.argv[1] in authorFlags):
        if (len(sys.argv) <= 3):
            displayAuthors(dataSource)
        else:
            statement = f'Usage: {sys.argv[0]} -a search_string \n'
            statement += 'searches and prints all authors in booksdatasource whose surname or given name contain search_string. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
    elif (sys.argv[1] in bookFlags):
        if (len(sys.argv) <= 4):
            displayBooks(dataSource)
        else:
            statement = f'Usage: {sys.argv[0]} -t search_string [title | year] \n'
            statement += 'searches and prints all books in booksdatasource whose title contains search_string. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
    elif (sys.argv[1] in yearFlags):
        if (len(sys.argv) <= 4):
            displayYears(dataSource)
        else:
            statement = f'Usage: {sys.argv[0]} -y start_year end_year \n'
            statement += '    searches and prints all books in booksdatasource published in or between start_year and end_year. \n \n'
            statement += f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'

def displayAuthors(dataSource):
    results = dataSource.authors(sys.argv[2])
    if (type(results[0]) == type(1)):
        reportError(results[1])
    for author in results:
        entry = f'{author.surname}, {author.given_name} ({author.birth_year}-{author.death_year}). \n'
        for book in author.writtenWorks:
            entry += f'        {formatBook(book, includeAuthor=False)}\n'
        print(entry)


def displayBooks(dataSource):
    if (len(sys.argv) == 3):
        results = dataSource.books(sys.argv[2])
    else:
        results = dataSource.books(sys.argv[2], sys.argv[3])

    if (type(results[0]) == type(1)):
        reportError(results[1])
    for book in results:
        print(formatBook(book))

def displayYears(dataSource):
    if (len(sys.argv) == 3):
        results = dataSource.books_between_years(sys.argv[2])
    else:
        results = dataSource.books_between_years(sys.argv[2], sys.argv[3])
    if (type(results[0]) == type(1)):
        reportError(results[1])
    for book in results:
        print(formatBook(book))

def formatBook(book, includeAuthor=True):
    entry = f'{book.title}'
    if(includeAuthor):
        entry += f', {book.authors[0].given_name} {book.authors[0].surname}'
        for i in range(1, len(book.authors)):
            entry += f" and {book.authors[i].given_name} {book.authors[i].surname}"
    entry += f', {book.publication_year}.'
    return entry

def reportError(message):
    print(message)
    sys.exit()

def getHelp():
    f = open('usage.txt', 'r')
    usageStatement = f.read()
    print(usageStatement)
    f.close()
    sys.exit()

def main():
    dataSource = booksdatasource.BooksDataSource('books1.csv')
    parseCommandLine(dataSource)


if __name__ == '__main__':
    main()

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
            statement += '    searches and prints all authors in booksdatasource whose surname or given name contain search_string. \n'
            statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)
    elif (sys.argv[1] in bookFlags):
        if (len(sys.argv) <= 4):
            displayBooks(dataSource)
        else:
            statement = f'Usage: {sys.argv[0]} -t search_string [title | year] \n'
            statement += '    searches and prints all books in booksdatasource whose title contains search_string. \n'
            statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)
    elif (sys.argv[1] in yearFlags):
        if (len(sys.argv) <= 4):
            displayYears(dataSource)
        else:
            statement = f'Usage: {sys.argv[0]} -y start_year end_year \n'
            statement += '    searches and prints all books in booksdatasource published in or between start_year and end_year. \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)
    else:
        print(f'Unrecognized Flag: {sys.argv[0]} {sys.argv[1]}')
        print(f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.')

def displayAuthors(dataSource):
    if (len(sys.argv) == 2):
        results = dataSource.authors()
    else:
        results = dataSource.authors(sys.argv[2])
    validateResults(results)
    for author in results:
        entry = f'{author.surname}, {author.given_name} ({author.birth_year}-{author.death_year}). \n'
        for book in author.writtenWorks:
            entry += f'        {formatBook(book, includeAuthor=False)}\n'
        print(entry)

def displayBooks(dataSource):
    if (len(sys.argv) == 2):
        results = dataSource.books()
    elif (len(sys.argv) == 3):
        results = dataSource.books(sys.argv[2])
    else:
        results = dataSource.books(sys.argv[2], sys.argv[3])
    validateResults(results)
    for book in results:
        print(formatBook(book))

def displayYears(dataSource):
    if (len(sys.argv) == 2):
        results = dataSource.books_between_years()
    elif (len(sys.argv) == 3):
        results = dataSource.books_between_years(sys.argv[2])
    else:
        results = dataSource.books_between_years(sys.argv[2], sys.argv[3])
    validateResults(results)
    for book in results:
        print(formatBook(book))

def validateResults(resultList):
    '''Insures the given list of results is not empty and not the result
        of an error (denoted by an int in the first element)
    '''
    if (len(resultList) < 1):
        print('No results were found for those search terms. Double check your search and try again.')
        print(f'or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.')
        sys.exit()
    if (type(resultList[0]) == type(1)):
        reportError(resultList[1])

def formatBook(book, includeAuthor=True):
    entry = f'"{book.title}"'
    if(includeAuthor):
        entry += f', {book.authors[0].given_name} {book.authors[0].surname}'
        for i in range(1, len(book.authors)):
            entry += f" and {book.authors[i].given_name} {book.authors[i].surname}"
    entry += f', {book.publication_year}.'
    return entry

def reportError(message):
    print(message)
    print(f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.')
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

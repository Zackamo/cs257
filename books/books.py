'''
    books.py
    Zack Johnson and Alia Babinet, September 30, 2021

    Searches the books data set using BooksDataSource.
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''
import booksdatasource
import sys

AUTHOR_FLAGS = ['-a','--search-author']
BOOK_FLAGS = ['-t','--search-title']
YEAR_FLAGS = ['-y','--search-year']
HELP_FLAGS = ['-h','-?','--help']

def validate_results(result_list):
    '''Insures the given list of results is not empty and not the result
        of an error (denoted by an int in the first element)
    '''
    if (len(result_list) < 1):
        report_error('No results were found for those search terms. If this was unexpected, double check your search and try again.')
    if (type(result_list[0]) == type(1)):
        report_error(result_list[1])

def display_authors(data_source):
    '''manages retrieving and displaying results of an author search
    '''
    if (len(sys.argv) == 2): # no search term given
        results = data_source.authors()
    else: # search term given
        results = data_source.authors(sys.argv[2])
    validate_results(results)
    for author in results:
        print(author)
        for book in author.written_works:
            print(f'        "{book.title}", {book.publication_year}')

def display_books(data_source):
    '''manages retrieving and displaying results of a title search
    '''
    if (len(sys.argv) == 2): # no Search Term given
        results = data_source.books()
    elif (len(sys.argv) == 3): # Search Term, but no Sorting Flag
        results = data_source.books(sys.argv[2])
    else: # both a Search term and Sorting Flag
        results = data_source.books(sys.argv[2], sys.argv[3])
    validate_results(results)
    for book in results:
        print(book)

def display_years(data_source):
    '''manages retrieving and displaying results of a publication year search
    '''
    if (len(sys.argv) == 2): # no Search Years given
        results = data_source.books_between_years()
    elif (len(sys.argv) == 3): # one Year given
        results = data_source.books_between_years(sys.argv[2])
    else: # both years given
        results = data_source.books_between_years(sys.argv[2], sys.argv[3])
    validate_results(results)
    for book in results:
        print(book)

def report_error(message):
    '''prints given error message plus direction to the --help
    '''
    print(message)
    print(f'Use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.')
    sys.exit()

def get_help(help_flag=None):
    ''' displays a helpful hint depending on the help flag or the entire
        documentation (reads and prints usage.txt) if no flag is given.
    '''
    if help_flag == 'author_search_help':
        statement = f'Usage: {sys.argv[0]} -a search_string \n'
        statement += '    searches and prints all authors in booksdatasource whose surname or given name contain search_string. \n'
        statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
        statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
        print(statement)

    elif help_flag == 'book_search_help':
        statement = f'Usage: {sys.argv[0]} -t search_string [title | year] \n'
        statement += '    searches and prints all books in booksdatasource whose title contains search_string. \n'
        statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
        statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
        print(statement)

    elif help_flag == 'year_search_help':
        statement = f'Usage: {sys.argv[0]} -y start_year end_year \n'
        statement += '    searches and prints all books in booksdatasource published in or between start_year and end_year. \n \n'
        statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
        print(statement)

    else:
        f = open('usage.txt', 'r')
        usage_statement = f.read()
        print(usage_statement)
        f.close()
        sys.exit()

def main():
    data_source = booksdatasource.BooksDataSource('books1.csv')
    if (sys.argv[1] in HELP_FLAGS or len(sys.argv) <= 1):
        get_help()

    elif (sys.argv[1] in AUTHOR_FLAGS):
        if (len(sys.argv) <= 3):
            display_authors(data_source)
        else:
            get_help('author_search_help')

    elif (sys.argv[1] in BOOK_FLAGS):
        if (len(sys.argv) <= 4):
            display_books(data_source)
        else:
            get_help('book_search_help')

    elif (sys.argv[1] in YEAR_FLAGS):
        if (len(sys.argv) <= 4):
            display_years(data_source)
        else:
            get_help('year_search_help')

    else:
        report_error(f'Unrecognized Flag: {sys.argv[0]} {sys.argv[1]}')


if __name__ == '__main__':
    main()

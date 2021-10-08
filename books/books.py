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
        report_error('No results were found for those search terms. Double check your search and try again.')
    if (type(result_list[0]) == type(1)):
        report_error(result_list[1])

def display_authors(data_source):
    '''manages retrieving and displaying results of an author search
    '''
    if (len(sys.argv) == 2):
        results = data_source.authors()
    else:
        results = data_source.authors(sys.argv[2])
    validate_results(results)
    for author in results:
        entry = f'{author.surname}, {author.given_name} ({author.birth_year}-{author.death_year}). \n'
        for book in author.written_works:
            entry += f'        {format_book(book, include_author=False)}\n'
        print(entry)

def display_books(data_source):
    '''manages retrieving and displaying results of a title search
    '''
    if (len(sys.argv) == 2):
        results = data_source.books()
    elif (len(sys.argv) == 3):
        results = data_source.books(sys.argv[2])
    else:
        results = data_source.books(sys.argv[2], sys.argv[3])
    validate_results(results)
    for book in results:
        print(format_book(book))

def display_years(data_source):
    '''manages retrieving and displaying results of a publication year search
    '''
    if (len(sys.argv) == 2):
        results = data_source.books_between_years()
    elif (len(sys.argv) == 3):
        results = data_source.books_between_years(sys.argv[2])
    else:
        results = data_source.books_between_years(sys.argv[2], sys.argv[3])
    validate_results(results)
    for book in results:
        print(format_book(book))

def format_book(book, include_author=True):
    ''' formats the given book as (default): "title", author and author, year.
        or, if includeAuthor is False, as: "title", year.
    '''
    entry = f'"{book.title}"'
    if(include_author):
        entry += f', {book.authors[0].given_name} {book.authors[0].surname}'
        for i in range(1, len(book.authors)):
            entry += f" and {book.authors[i].given_name} {book.authors[i].surname}"
    entry += f', {book.publication_year}.'
    return entry

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
    match help_flag:
        case 'author_search_help':
            statement = f'Usage: {sys.argv[0]} -a search_string \n'
            statement += '    searches and prints all authors in booksdatasource whose surname or given name contain search_string. \n'
            statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)

        case 'book_search_help':
            statement = f'Usage: {sys.argv[0]} -t search_string [title | year] \n'
            statement += '    searches and prints all books in booksdatasource whose title contains search_string. \n'
            statement += '    if search_string contains spaces, enclose it in quotes e.g: "long string". \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)

        case 'year_search_help':
            statement = f'Usage: {sys.argv[0]} -y start_year end_year \n'
            statement += '    searches and prints all books in booksdatasource published in or between start_year and end_year. \n \n'
            statement += f'Or use: {sys.argv[0]} -? or {sys.argv[0]} --help for more information.'
            print(statement)

        case _:
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

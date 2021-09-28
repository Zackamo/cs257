#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.writtenWorks = []

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.authorList = []
        self.bookList = []
        with open(books_csv_file_name) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                thisAuthor = parseAuthorString(self, row[2])
                newBook = Book(row[0], row[1], thisAuthor)
                self.bookList.append(newBook)
                for curAuthor in thisAuthor:
                    print(thisAuthor)
                    curAuthor.writtenWorks.append(newBook)

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        return []

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''

        return []

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        return []

def newAuthor(self, lastName, firstName, years):
    ''' Returns an author object corresponding to the information given. If an author by the
        given name and surname already exists in the authorList, return it. Otherwise add the
        new author to the authorList and return it.
    '''
    yearList = years[1 : -1].split("-")
    birthYear, deathYear = yearList[0], yearList[1]
    author = Author(lastName, firstName, birthYear, deathYear)

    for curAuthor in self.authorList:
        if (curAuthor == author):
            print("curAuthor" , curAuthor.surname)
            return curAuthor
        else:
            self.authorList.append(author)
            print("in else of curAuthor loop")
            print("author" , author.surname)
            return author

def parseAuthorString(self, authorString):
    ''' Returns an Author object corresponding to the given string:
        Parses a string containing an authors First and Last names, separated by spaces
        followed by birth and death years of the form (birth-death) or (birth-).
    '''
    authors = []
    splitAuthor = authorString.split(' ')
    splitSize = len(splitAuthor)
    if (splitSize == 3):
        print ("splitSize = 3")
        author = newAuthor(self, splitAuthor[1],splitAuthor[0],splitAuthor[2])
        print (author.surname)
        authors.append(author)

    elif (splitSize == 4):
        authors.append(newAuthor(self, splitAuthor[2],splitAuthor[0]+' '+splitAuthor[1],splitAuthor[3]))
    elif (splitSize >= 5):
        print("Multi-Author book")
    return authors

if __name__ == "__main__":
    ds = BooksDataSource("books1test.csv")

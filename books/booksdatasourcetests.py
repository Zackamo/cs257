'''
   booksdatasourcetest.py
   Alia Babinet, Zack Johnson, 25 September 2021
   From a template by Jeff Ondich
'''

from booksdatasource import BooksDataSource, Author, Book
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1test.csv')

    def tearDown(self):
        pass

######### Initialization Tests ########

    def test_initialisation(self):
        books = self.data_source.bookList
        authors = self.data_source.authorList
        self.assertTrue(len(books) == 8)
        self.assertTrue(len(authors) == 8)

######### Author Tests ###########

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_multi_author(self):
        authors = self.data_source.authors('Bront')
        self.assertTrue(len(authors) == 3)
        self.assertTrue(authors[0] == Author('Brontë','Ann'))
        self.assertTrue(authors[1] == Author('Brontë','Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë','Emily'))

    def test_capitals_author(self):
        authors = self.data_source.authors('praTcHett')
        self.assertTrue(len(authors) == 1)
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_empty_author(self):
        authors = self.data_source.authors('')
        self.assertTrue(len(authors) == 6)
        self.assertTrue(authors[0] == Author('Brontë','Ann'))
        self.assertTrue(authors[1] == Author('Brontë','Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë','Emily'))

    def test_missing_author(self):
        authors = self.data_source.authors('broq')
        self.assertTrue(len(authors) == 0)
        

######### Title Tests ##########

    def test_unique_title(self):
        titles = self.data_source.books('Ho,')
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0] == Book('Right Ho, Jeeves'))

    def test_multi_byTitle(self):
        titles = self.data_source.books('il','title')
        self.assertTrue(len(titles) == 2)
        self.assertTrue(titles[0] == Book('The Tenant of Wildfell Hall'))
        self.assertTrue(titles[1] == Book('Villette'))

    def test_multi_byYear(self):
        titles = self.data_source.books('er','title')
        self.assertTrue(len(titles) == 4)
        self.assertTrue(titles[3] == Book('Neverwhere'))
        self.assertTrue(titles[0] == Book('Wuthering Heights'))
        self.assertTrue(titles[2] == Book('Hard-Boiled Wonderland and the End of the World'))
        self.assertTrue(titles[1] == Book('Elmer Gantry'))

    def test_missing_title(self):
        titles = self.data_source.books('Hello')
        self.assertTrue(len(titles) == 0)


######### Year Tests ###########

    def test_multiRange(self):
        books = self.data_source.books_between_years(1846, 1849)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Wuthering Heights'))
        self.assertTrue(books[1] == Book('The Tenant of Wildfell Hall'))

    def test_onEndYear(self):
        books = self.data_source.books_between_years(1927, 1934)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Elmer Gantry'))
        self.assertTrue(books[1] == Book('Right Ho, Jeeves'))

    def test_none(self):
        books = self.data_source.books_between_years(1750, 1790)
        self.assertTrue(len(books) == 0)

    def test_tie(self):
        books = self.data_source.books_between_years(1995, 2000)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Neverwhere'))
        self.assertTrue(books[1] == Book('Thief of Time'))

    def test_onlyStartYear(self):
        books = self.data_source.books_between_years(1995)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Neverwhere'))
        self.assertTrue(books[1] == Book('Thief of Time'))

    def test_onlyEndYear(self):
        books = self.data_source.books_between_years(end_year=1850)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Wuthering Heights'))
        self.assertTrue(books[1] == Book('The Tenant of Wildfell Hall'))

    def test_badArg(self):
        #not totally sure what would happen here...
        books = self.data_source.books_between_years("", 1850)
        self.assertTrue(len(books) == 2)
        self.assertTrue(books[0] == Book('Neverwhere'))
        self.assertTrue(books[1] == Book('Thief of Time'))
if __name__ == '__main__':
    unittest.main()


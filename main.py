# Import get() method from request package -> get URL info; codes to very if the request is successful
from requests import get, codes
# Import BeautifulSoup method from bs4 -> Scrap web
from bs4 import BeautifulSoup
# Import loads() method from json -> Work with JSON object from OpenLibra's API
from json import loads
# Import randint() method from random -> Generate random number between 1 - 3 to assign tier to books
from random import randint
# Import MySQL class
from my_sql import *
# Import sleep() method from time -> If get() response is not successful, sleep 3 seconds because the page might have some server error (pretty common in OpenLibra)
from time import sleep

def gen_random_tier() -> int:
    # Free tier - 1 ; Pro Tier - 2, Premium Tier - 3
    # Generate a random value to assign tier to each book
    return randint(1, 3)


def get_book_content(url:str) -> dict:
    while True:
        get_url = get(url)

        # Check Response Code
        if get_url.status_code != codes.ok: # Check if the request wasnt successful
            sleep(3)
            continue
        else:
            page = get_url.text # Get HTML content

            soup = BeautifulSoup(page, 'html.parser') # Create the scrapper html parser

            # # Check if the Dowload button has the property 'data-action="download-warning"' that we are interested on
            # if soup.select('a[title="Download Book (SHIFT + S)"]')[0].get('data-action') != "download-warning":
            #     return

            select_title = soup.select('.book-cover-wrapper > img')
            if len(select_title) == 0:
                return {}

            title = select_title[0].get('alt') # Select the Title element

            # Verify (just in case) if the API url exists
            get_book_api = get(f'https://www.etnassoft.com/api/v1/get/?book_title="{title}"')
            if get_book_api.status_code == codes.ok:
                book_api = loads(get_book_api.text)

                if len(book_api) == 0:
                    return {}

                # Remove "\r\n" characters from description
                descr = str(book_api[0]['content']).replace("\r\n\r\n", " ")


                # Create a Dictionary with all info needed about the book 
                book = {
                    "ID": int(book_api[0]['ID']), # Book's ID
                    "title": book_api[0]['title'], # Book's Title
                    "author": book_api[0]['author'], # Book's Author ID -> Note that (repeating) the relation between tables is set to 1-N instead of N-N because of OpenLibra's authors system
                    "description": descr, # Book's Description
                    "publisher": book_api[0]['publisher'], # Book's Publisher
                    "year": int(book_api[0]['publisher_date']), # Book's publication year -> publisher year
                    "pages": int(book_api[0]['pages']), # Book's number of pages
                    "lang": book_api[0]['language'], # Book's language
                    "categories": book_api[0]['categories'], # Book's Categories List turned into str
                    "cover": book_api[0]['cover'], # Book's Cover
                    "cover_extension": book_api[0]['cover'].split(".")[-1], # Book's Cover extension for saving file (future)
                    "thumbnail": book_api[0]['thumbnail'], # Book's Thumbnail (smaller cover image)
                    "thumbnail_extension": book_api[0]['thumbnail'].split(".")[-1], # Book's Thumbnail extension for saving file (future)
                    "pdf": soup.select('a[title="Download Book (SHIFT + S)"]')[0].get('href'),
                    "tier": gen_random_tier()
                }
                
                # Return the Book's dictionary
                return book
            else:
                # Void return in case the API connection didn't work
                return {}


def dict_to_sql(book:dict) -> None:
    global mysql

    if book == {}: # Empty book
        return
    
    # Chech if book already exists in databse
    if len(mysql.select_book_by_id(book['ID'])) != 0:
        return

    # Check if author's name is alredy registered
    # ? Remember that some authors might be repeated because of OpenLibra's API no author registration system
    is_auth = mysql.select_author_by_name(book['author'])
    if len(is_auth) == 1:
        mysql.update_authors_n_books(is_auth[0][0])
        auth_id = is_auth[0][0]
    else:
        mysql.insert_author(book['author'])
        auth_id = mysql.select_author_by_name(book['author'])[0][0]


    # Check if categories are already registered
    for c in book['categories']:
        is_cat = mysql.select_category_by_id(c['category_id'])

        if len(is_cat) == 1:
            mysql.update_cat_n_books(c['category_id'])
        else:
            mysql.insert_category(c['category_id'], c['nicename'])
        
    # Insert Book
    mysql.insert_book(book['ID'], book['title'], auth_id, book['publisher'], book['year'], book['lang'], book['description'], book['pages'], book['cover'], book['thumbnail'], book['pdf'], book['tier'])

    # Insert BooksCategories data
    for c in book['categories']:
        mysql.insert_book_category(book['ID'], c['category_id'])

    



if __name__ == "__main__":
    # Define MySQL Server parameters:
    # schema = 'testLibrary' # TEST DB -> connection test
    schema = 'Library' # Final DB
    host = '192.168.56.100' # VM's IP

    # Create the object instance for SQL methods
    mysql = MySQL(host, schema)

    # # TEST CONNECTION
    # test = mysql.test() # Returns a list of tuples

    # print(test)
    # print(test[0][0])
    # print(len(test) == 0)

    # get_url = get_book_content("https://openlibra.com/en/book/a-graduate-course-in-applied-cryptography")
    # dict_to_sql(get_url)


    # Open & close the CSV file & store all URL in a single list
    books = open("url.csv", mode='r', encoding='utf-8-sig')
    books_list = books.read().split("\n")
    books.close()
    # Remove the last element since it is empty
    books_list.pop()

    for b in books_list:
        dict_to_sql(get_book_content(b))
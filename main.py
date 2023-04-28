# Import get() method from request package -> get URL info; codes to very if the request is successful
from requests import get, codes
# Import BeautifulSoup method from bs4 -> Scrap web
from bs4 import BeautifulSoup
# Import loads() method from json -> Work with JSON object from OpenLibra's API
from json import loads
# Import randint() method from random -> Generate random number between 1 - 3 to assign tier to books
from random import randint

def gen_random_tier() -> int:
    # Free tier - 1 ; Pro Tier - 2, Premium Tier - 3
    # Generate a random value to assign tier to each book
    return randint(1, 3)

    

def get_book_content(url:str) -> dict:
    get_url = get(url)
    if get_url.status_code == codes.ok: # Check if the request was successful
        page = get_url.text # Get HTML content

        soup = BeautifulSoup(page, 'html.parser') # Create the scrapper html parser

        # # Check if the Dowload button has the property 'data-action="download-warning"' that we are interested on
        # if soup.select('a[title="Download Book (SHIFT + S)"]')[0].get('data-action') != "download-warning":
        #     return

        selct_title = soup.select('.book-cover-wrapper > img')
        if len(selct_title) == 0:
            return {}

        title = selct_title[0].get('alt') # Select the Title element

        # Verify (just in case) if the API url exists
        get_book_api = get(f'https://www.etnassoft.com/api/v1/get/?book_title="{title}"')
        if get_book_api.status_code == codes.ok:
            book_api = loads(get_book_api.text)

            if len(book_api) == 0:
                return {}

            # Remove "\r\n" characters from description
            descr = str(book_api[0]['content']).replace("\r\n\r\n", " ")

            # Check if Authors or Categories return 0, and if so set a default value
            author_id = write_authors_name(book_api[0]['author'])

            categories_list_str =  return_categories_list_str(book_api[0]['categories'])

            # Create a Dictionary with all info needed about the book 
            book = {
                "ID": book_api[0]['ID'], # Book's ID
                "title": book_api[0]['title'], # Book's Title
                "author": author_id, # Book's Author ID -> Note that (repeating) the relation between tables is set to 1-N instead of N-N because of OpenLibra's authors system
                "description": descr, # Book's Description
                "publisher": book_api[0]['publisher'], # Book's Publisher
                "year": book_api[0]['publisher_date'], # Book's publication year -> publisher year
                "pages": book_api[0]['pages'], # Book's number of pages
                "lang": book_api[0]['language'], # Book's language
                "categories": categories_list_str, # Book's Categories List turned into str
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



if __name__ == "__main__":
    # Open & close the CSV file & store all URL in a single list
    books = open("url.csv", mode='r', encoding='utf-8-sig')
    books_list = books.read().split("\n")
    books.close()
    # Remove the last element since it is empty
    books_list.pop()

# Import get() method from request package -> get URL info; codes to very if the request is successful
from requests import get, codes
# Import BeautifulSoup method from bs4 -> Scrap web
from bs4 import BeautifulSoup
# Import loads() method from json -> Work with JSON object from OpenLibra's API
from json import loads
def get_book_content(url:str) -> dict:
    get_url = get(url)
    if get_url.status_code == codes.ok: # Check if the request was successful
        page = get_url.text # Get HTML content

        soup = BeautifulSoup(page, 'html.parser') # Create the scrapper html parser
        title = soup.select(
            '.book-cover-wrapper > img')[0].get('alt').lower() # Select the Title element and turn lower case

        get_book_api = loads(get(
            f'https://www.etnassoft.com/api/v1/get/?book_title="{title}"').text) # API connection

        
        book_id = get_book_api[0]['ID'] # Book's ID
        book_title = get_book_api[0]['title'] # Book's Title
        author_name = get_book_api[0]['author'] # Book's Author -> cannot access to author_id, so queries will be based on author's name (using LIKE)
        description = get_book_api[0]['content'] # Book's Description
        publisher = get_book_api[0]['publisher'] # Book's Publisher
        year = get_book_api[0]['publisher_date'] # Book's publication year -> publisher year
        n_pages = get_book_api[0]['pages'] # Book's number of pages
        lang = get_book_api[0]['language'] # Book's language
        categories = get_book_api[0]['categories'] # Book's Categories List
        # Book's Cover Image URL
        cover = get_book_api[0]['cover']
        cover_extension = cover.split(".")[-1]
        # Book's Thumbnail Image URL
        thumbnail = get_book_api[0]['thumbnail']
        thumbnail_extension = thumbnail.split(".")[-1]
        # Book's PDF URL
        download_url = soup.select('a[title="Download Book (SHIFT + S)"]')[0].get('href')


        # Return a dictionary with all information 
        book = {
            "id": book_id,
            "title": book_title,
            "author": author_name,
            "description": description,
            "publisher": publisher,
            "year": year,
            "pages": n_pages,
            "lang": lang,
            "categories": categories,
            "cover": cover,
            "thumbnail": thumbnail,
            "pdf": download_url
        }
        
        return book



if __name__ == "__main__":
    # Open the CSV file & store all URL in a single list
    # books = list(open("books.csv", "r").read().split("\n"))
    # Remove the last element since it is empty
    # books.pop()

    test = get_book_content("https://openlibra.com/en/book/interface-circuits-for-microsensor-integrated-systems-2")
    print(test)
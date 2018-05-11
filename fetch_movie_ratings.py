'''
'''
from bs4 import BeautifulSoup
import requests

def search_movie(*args):
    '''
    Seach for a movie by its name on IMDb
    '''
    
    print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*58))
    print("| {0:^10} | {1:^30} | {2:^10} |".format("Sr. No.", "Title", "Ratings"))
    print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*58))

    for title in args:
        # Get url
        url = get_url(title)
        
        # Get the data
        response = simple_get(url)
        if response is not None:
            html = BeautifulSoup(response, 'html.parser')
            body = html.find('body')

            # Get the tags that contains movies title
            searched_movie_titles = body.find_all('h3', attrs={'class':'lister-item-header'})
            # Get the tags that contains movies rating
            searched_movie_ratings = body.find_all('div', attrs={'class':'ratings-imdb-rating'})
            # Loop through each title to find the exact match & so its rating
            match = False
            for title_index in range(len(searched_movie_titles)):
                if is_movie_found(title, searched_movie_titles, title_index):
                    print("| {0:^10} | {1:<30} | {2:<10} |".format(title, searched_movie_ratings[title_index].get('data-value')))
                    match = True
                    break
            # Report if the searched movie is not present on IMDb 
            if not match:
                log_error("Bad luck! \'%s\' is unavailable, Please try again!" %title)

def is_movie_found(title, searched_movie_titles, title_index):
    return ''.join(list(searched_movie_titles[title_index].children)[3].get_text().lower().strip().split()).startswith(''.join(title.lower().split()))

def get_url(title):
    '''
    Simply constructs the url by concatenating title with the base url
    '''
    return "https://www.imdb.com/search/title?title=" + '+'.join(title.split())

def simple_get(url):
    '''
    It gets the content at 'url' by making an HTTP/GET request
    '''
    try:
        page = requests.get(url)
        if is_response_good(page):
            return page.content
        else:
            return None
    except RequestException as e:
        log_error("Error during request to {0} : {1}".format(url, str(e)))

def is_response_good(response):
    '''
    Validate the response
    '''
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(error):
    '''
    Simply prints the error message.
    '''
    print(error)

if __name__ == '__main__':
    search_movie("The Godfather", "Star Trek", "The Lord Of The Rings", "The Wolf Of Wall Street", "The Godfather II", "Padmavati", "Annabelle: Creation")
    search_movie("The GodFaTher III")
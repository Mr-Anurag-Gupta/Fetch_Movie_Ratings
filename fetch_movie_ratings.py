'''
'''
from bs4 import BeautifulSoup
import requests

def search_movie(titles):
    '''
    Seach for a movie by its name on IMDb
    '''
    
    print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))
    print("| {0:^10} | {1:^30} | {2:^10} | {3:^20} |".format("Sr. No.", "Title", "Ratings", "Availability"))
    print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))

    for index in range(len(titles)):
        # Get url
        url = get_url(titles[index])
        
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
                if is_movie_found(titles[index], searched_movie_titles, title_index):
                    print("| {0:^10} | {1:<30} | {2:^10} | {3:^20} |".format(index+1, titles[index], searched_movie_ratings[title_index].get('data-value'), "(available)"))
                    print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))
                    match = True
                    break
            # Report if the searched movie is not present on IMDb 
            if not match:
                print("| {0:^10} | {1:<30} | {2:^10} | {3:^20} |".format(index+1, titles[index], '---', "(unavailable)"))
                print("{plus}{hyphens}{plus}".format(plus = '+', hyphens = '-'*81))

def is_movie_found(title, searched_movie_titles, title_index):
    '''
    Checks the availability of a movie on the IMDb website.
    Returns True if movie is available, False otherwise.
    '''
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
        log_error_msg("Error during request to {0} : {1}".format(url, str(e)))

def is_response_good(response):
    '''
    Validate the response
    '''
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error_msg(error):
    '''
    Simply prints the error message.
    '''
    print(error)

if __name__ == '__main__':
    movies = input("\nEnter movie(s) name ( without quotes )\n( Movies names must be (,) seperated ): ").split(',')
    movies = [title.strip() for title in movies]
    search_movie(movies)
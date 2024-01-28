# arXiv API
# Programmer: Indrajit Ghosh
# Date: Nov 12, 2021
# API Website: https://arxiv.org/help/api/user-manual

import requests, bs4, os

def show_results(entries):

    print()
    print('\t\tResults')
    print()

    print('-' * 50)

    for entry in entries:
        print('.'*80)

        title = entry.title.text
        
        published = entry.published.text[:10]

        authors = entry.findAll('author')
        auth_str = ''
        for auth in authors:
            auth_str += auth.find('name').text + ', '
        auth_str = auth_str[:-2]

        pdf_link = str(entry.select('link')[1])[11:].split('rel=')[0]

        print(f'\nTitle: {title}')
        print(f'\nPublished date: {published}')
        print(f'\nAuthor(s): {auth_str}')
        print(f'\nPdf link: {pdf_link}')

        print()
        print('.' * 60)
        print('\n\n')



if __name__ == '__main__':

    os.system('clear')

    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?'

    # Search parameters
    search_text = input('Enter your search query: ')
    search_query = f'all:{search_text}' # search for electron in all fields
    start = 0                     # retreive the first 5 results
    max_results = 5

    # sortBy can be "relevance", "lastUpdatedDate", "submittedDate"
    sortBy = 'submittedDate'
    # sortOrder can be either "ascending" or "descending"
    sortOrder = 'descending'

    query = f'search_query={search_query}&start={start}&max_results={max_results}'
    # query = f'search_query={search_query}&start={start}&max_results={max_results}&sortBy={sortBy}&sortOrder={sortOrder}'

    url = base_url + query

    res = requests.get(url)
    res.raise_for_status()
    
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Entries
    entries = soup.findAll('entry')

    show_results(entries)


    


    
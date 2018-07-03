import pandas as pd
import requests
from bs4 import BeautifulSoup

# import podcasts csv file and extract urls
podcasts = pd.read_csv('../data/itunes-podcast-list-UNDUP.csv')
itunes_link = podcasts.iloc[:,0]

# loop through url list to scrape each podcast page
for i in range(len(itunes_link)):
    print(podcasts.iloc[:,1][i])
    print(itunes_link)
    try:
        page = requests.get(itunes_link[i]).text
    except requests.exceptions.Timeout:
        print('The request for a page at {} timed out...skipping.'.format(itunes_link[i])),
        continue
    except requests.exceptions.HTTPError as e: 
        print(e),
        continue

    soup = BeautifulSoup(page, 'html.parser')

    podcast_id = i
    podcast_url = itunes_link[i]
    podcast_name = podcasts.iloc[:,1][i]
    podcast_descr = []
    podcast_img = []
    podcast_category = []
    podcast_language = []
    podcast_rating_score = []
    podcast_rating_count = []
    podcast_website = []
    episode_name = []
    episode_date = []
    episode_descr = []

    # extract podcast details
    titlebox = soup.find('div', {'class': 'product-review'})
    if titlebox == None:
        descr = ''
    else:
        descr = titlebox.find('p').text
    podcast_descr.append(descr)

    art = soup.find('div', {'class': 'artwork'})
    if art == None:
        img = ''
    else:
        img = art.find('img')['src']
    podcast_img.append(img)

    category = soup.find('li', {'class': 'genre'})
    if category == None:
        cat = ''
    else:
        cat = category.text
    podcast_category.append(cat)

    language = soup.find('li', {'class': 'language'})
    if language == None:
        lang = ''
    else:
        lang = language.text
    podcast_language.append(lang)

    score = soup.find('span', {'itemprop': 'ratingValue'})
    if score == None:
        rtg = ''
    else:
        rtg = score.text
    podcast_rating_score.append(rtg)

    count = soup.find('span', {'class': 'rating-count'})
    if count == None:
        num = ''
    else:
        num = count.text
    podcast_rating_count.append(num)

    links = soup.find('div', {'metrics-loc': 'Titledbox_Links'})
    if links == None:
        site = ''
    else:
        site = links.find('a')['href']
    podcast_website.append(site)

    # extract episodes details
    for name_col in soup.findAll('td', {'class': 'name flexible-col'}):
        name = name_col.find('span', {'class': 'text'}).text
        episode_name.append(name)

    for date_col in soup.findAll('td', {'class': 'release-date'}):
        try:
            date = date_col.find('span', {'class': 'text'}).text
        except AttributeError:
            date = ''
        episode_date.append(date)

    for descr_col in soup.findAll('td', {'class': 'description flexible-col'}):
        try:
            descr = descr_col.find('span', {'class': 'text'}).text
        except AttributeError:
            descr = ''
        episode_descr.append(descr)

    if len(episode_date) == 0:
        episode_date = ''

    if episode_descr == 0:
        episode_descr = ''

    # create podcast details and episodes list dataframes and export to csv
    podcast_details = pd.DataFrame({'a': podcast_id,
                                    'b': podcast_url,
                                    'c': podcast_name,
                                    'd': podcast_descr,
                                    'e': podcast_img,
                                    'f': podcast_category,
                                    'g': podcast_language,
                                    'h': podcast_rating_score,
                                    'j': podcast_rating_count,
                                    'k': podcast_website})

    episode_list = pd.DataFrame({'l': podcast_id,
                                 'm': podcast_name,
                                 'n': episode_name,
                                 'o': episode_date,
                                 'p': episode_descr})

    podcast_details.drop_duplicates(keep='first')
    episode_list.drop_duplicates(keep='first')

    with open('itunes-podcast-details.csv', 'a') as f1:
        podcast_details.to_csv(f1, header=False, index=False, encoding='utf-8')

    with open('itunes-podcast-episodes.csv', 'a') as f2:
        episode_list.to_csv(f2, header=False, index=False, encoding='utf-8')


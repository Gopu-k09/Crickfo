from django.shortcuts import render
from .models import Cricketer
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from .forms import ScrapeForm
import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from .models import Cricketer


def home_view(request):
    cricketers = Cricketer.objects.all()
    return render(request, 'cricketers/cricketer_list.html', {'cricketers': cricketers})

def scrape_data_view(request):
    if request.method == 'POST':
            form = ScrapeForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                p_fullname=soup.find('article',class_='w-player-bio__article w-player-bio__article--personal-details').find('ul',class_='w-player-bio__list').find_all('li',class_='w-player-bio__item')[0].get_text(strip=True).replace('Full Name', '').strip()
                basicinfo=soup.find('div',class_='w-player-header__player-details')
                p_country=basicinfo.find('div',class_='w-player-header__player-team').get_text(strip=True)
                p_position=basicinfo.find('p',class_='w-player-header__player-position js-player-type').get_text(strip=True)
                p_image_source=soup.find('img',class_='w-player-header__player-headshot u-hide-tablet')
                p_image_url=p_image_source['src']
                p_image_dynamic_number=p_image_source['data-id']+'-camedia.png'
                p_image = 'https:'+str(re.sub(r'placeholder\.png$', p_image_dynamic_number, str(p_image_url)))
                p_fname=soup.find('h1', {'id': 'tab-title'}).contents[0].strip()
                p_lname=soup.find('h1',{'id': 'tab-title'}).find('span').text
                p_story_source=soup.find('div',class_='w-player-bio__bio cms-content').find_all('p')

                p_cricket_source_summary=soup.findAll('table',class_='w-player-stats__table o-table__table w-player-stats__table--batting-summary')[0]
                p_cricket_source=p_cricket_source_summary.find('tbody',class_='o-table__table-body')
                p_odi_source=p_cricket_source.find_all('tr',class_='o-table__table-row')[0]
                p_odi_info=p_odi_source.find_all('td',class_='w-player-stats__table-cell o-table__table-cell')

                if Cricketer.objects.filter(fullname=p_fullname).exists():
                    print(f"{p_fullname} already exists in the database.")
                else:
                    cricketer=Cricketer()
                    cricketer.fullname=p_fullname
                    cricketer.country=p_country
                    cricketer.position=p_position
                    cricketer.image=p_image
                    cricketer.fname=p_fname
                    cricketer.lname=p_lname
                    cricketer.odi_matches=int(p_odi_info[0].text)
                    cricketer.odi_runs=int(p_odi_info[2].text.replace(',',''))
                    cricketer.odi_average=float(p_odi_info[4].text)
                    cricketer.odi_strike_rate=float(p_odi_info[7].text)
                    cricketer.odi_catches=int(p_odi_info[-2].text)
                    cricketer.story=p_story_scrape(p_story_source)
                    cricketer.url_source=url
                    cricketer.save()
                    print(f"{p_fullname} added in the database.")
                return redirect('home')
    else:
        form = ScrapeForm()
        return render(request, 'scrape/scrape_data.html', {'form': form})

def p_story_scrape(p_story_source):
    p_story=''
    for i in p_story_source:
        p_story+=str(i.text)
    return p_story

def get_player_data():
    players = Cricketer.objects.all()
    data = []
    for player in players:
        data.append([
            player.fullname,
            player.odi_matches,
            player.odi_runs,
            player.odi_average,
            player.odi_strike_rate,
            player.odi_catches
        ])
    return np.array(data)

def preprocess_data(data):
    scaler = MinMaxScaler()
    features = data[:, 1:].astype(float)  # Extract features (ignore names)
    normalized_features = scaler.fit_transform(features)
    return normalized_features, data[:, 0]  # Return features and names

def rank_players(features, names):
    # Assuming equal weights for simplicity
    weights = np.array([1, 1, 1, 1, 0.5])  # Adjust weights if necessary
    scores = np.dot(features, weights)
    ranked_players = sorted(zip(scores, names), reverse=True)[:6]
    return [name for score, name in ranked_players]

def top_six_player_view(request):
    data = get_player_data()
    features, names = preprocess_data(data)
    top_six_players = rank_players(features, names)
    return render(request, 'cricketers/top_six_players.html', {'top_six_players': top_six_players})

     

# def scrape_data_view(request):
#     try:
#         if request.method == 'POST':
#             form = ScrapeForm(request.POST)
#             if form.is_valid():
#                 url = form.cleaned_data['url']
#                 # Perform the scraping
#                 response = requests.get(url)
#                 soup = BeautifulSoup(response.text, 'html.parser')

#                 print(soup)

#                 # Clear existing records to avoid duplicates
#                 # Cricketer.objects.all().delete()

#                 fullname=soup.find('article',class_='w-player-bio__article w-player-bio__article--personal-details')
#                 movie_outline=soup.find('div',class_='synopsis-wrap').find_all('rt-text')[1]

#                 # print(fullname.text)
#                 # Scrape and save the data (modify the selectors as per the actual site structure)
#                 # for cricketer_data in soup.select('.cricketer'):
#                 #     name = cricketer_data.select_one('.name').text
#                 #     country = cricketer_data.select_one('.country').text
#                 #     runs = int(cricketer_data.select_one('.runs').text)
#                 #     wickets = int(cricketer_data.select_one('.wickets').text)

#                 #     Cricketer.objects.create(
#                 #         name=name,
#                 #         country=country,
#                 #         runs=runs,
#                 #         wickets=wickets
#                 #     )

#                 return redirect('home')
#         else:
#             form = ScrapeForm()
#         return render(request, 'scrape/scrape_data.html', {'form': form})
    
#     except Exception as e:
#         return e

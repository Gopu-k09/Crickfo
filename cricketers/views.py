from django.shortcuts import render
from .models import Cricketer
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from .forms import ScrapeForm
import re

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
                    cricketer.save()
                    print(f"{p_fullname} added in the database.")

                return redirect('home')
    else:
        form = ScrapeForm()
        return render(request, 'scrape/scrape_data.html', {'form': form})


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

from django.shortcuts import render
from .models import Search
# for Web-scrapping
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup

BASE_CRAIGSLIST_URL = 'https://chandigarh.craigslist.org/search/?query={}'
IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, template_name='base.html')

def new_search(request):

    if request.method == "POST":
        searched = request.POST.get("search")
        Search.objects.create(search=searched)

        final_url = BASE_CRAIGSLIST_URL.format(quote_plus(searched))

        # # scrapping part
        response = requests.get(final_url)
        data = response.text
        
        soup = BeautifulSoup(data, features='html.parser')
        post_list = soup.find_all('li', {'class': 'result-row'})

        final_postings = []
        for post in post_list:
            post_title = post.find(class_='result-title').text
            post_url = post.find('a').get('href')

            # price
            if (post.find(class_='result-price')):
                post_price = post.find(class_='result-price').text
            else:
                post_price = 'N/A'

            # image
            if (post.find(class_='result-image').get('data-ids')):
                post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                post_image_url = IMAGE_URL.format(post_image_id)
            else:
                post_image_url = 'https://craigslist.org/images/peace.jpg'

            final_postings.append((post_title, post_url, post_price, post_image_url))

        stuff_for_frontend = {'search':searched, 'final_postings':final_postings}

        return render(request, 'craigslist_app/new_search.html', stuff_for_frontend)
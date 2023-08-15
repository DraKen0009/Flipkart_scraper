import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render

from .forms import UrlForm
from .models import Data


# Create your views here.

def create_data(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            url = request.POST['url']
            respond = requests.get(url=url)
            content = respond.content
            soup = BeautifulSoup(content, 'html.parser')

            try:
                title = soup.find('span', class_='B_NuCI').text
                price = soup.find('div', class_='_30jeq3 _16Jk6d').text.replace(",", '')[1:]
                description = soup.find('div', class_='_2o-xpa').text
                num_media = len(soup.find_all('li', class_='_20Gt85 _1Y_A6W'))
                ratings = soup.find('div', class_='_2d4LTz').text
                num_rr = soup.find_all('div', class_='row _2afbiS')
                num_reviews = num_rr[1].find(name='span').text.split(" ")[0].replace(",", '')
                num_ratings = num_rr[0].find(name='span').text.split(" ")[0].replace(",", '')


            except:
                return HttpResponse('Incorrect url')

            if not Data.objects.filter(url=url, user=request.user).count() == 0:
                return HttpResponse('Data for the product already Exist')

            Data.objects.create(
                user=request.user,
                title=title,
                price=price,
                description=description,
                num_media=num_media,
                ratings=ratings,
                num_reviews=num_reviews,
                num_ratings=num_ratings,
                url=url
            )

            return HttpResponse('Data Stored in Database')
        else:

            return HttpResponse(f'Form Error : {form.errors.as_data()["url"][0]}')

    form = UrlForm()

    context = {
        'form': form
    }
    return render(request, 'scraper/create.html', context=context)

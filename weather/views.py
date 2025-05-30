import requests
from django.shortcuts import render
from .forms import CityForm
from timezonefinder import TimezoneFinder
from datetime import datetime   
import pytz

API_KEY = '8fb71fd013189ea125a0498ace28fab1'

def get_weather(request):
    time = None
    temp = None
    city = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get('cod') == 200:
                temp = data['main']['temp']

                lat = data['coord']['lat']
                lon = data['coord']['lon']

                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lat=lat, lng=lon)

                if timezone_str:
                    tz = pytz.timezone(timezone_str)
                    time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            else:
                temp = 'City not found'

    else:
        form = CityForm()

    return render(request, 'weather/home.html', {
        'form': form,
        'city': city,
        'temp': temp,
        'time': time
    })
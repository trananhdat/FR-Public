import json
import requests
import geocoder
from PIL import ImageTk
import base64, PIL, urllib, tkinter as tk

import io
import base64
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen

api_key = '1777e1c6994c63ad16f9ae8012ee46f1'

def Weather():

    lat, lon = geocoder.ip('me').latlng

    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(lat, lon, api_key)
    
    response = requests.get(url)
    data = json.loads(response.text)
    temp = round(float(data['main']['temp']) - 273)
    name =  data['name']
    icon = data['weather'][0]['icon']
    # image_url = 'http://openweathermap.org/img/wn/{}@2x.png'.format(icon)
    
    # image_byt = urlopen(image_url).read()
    # image_b64 = base64.encodestring(image_byt)
   
    return name, temp

# print(Weather())
import time
import requests
from PIL import Image
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?lat=50.04937&lon=10.22175&appid=c9d90dffca3619df2802e8c042def487&units=metric"
#Schweinfurt lat=50.04937&lon=10.22175

final_url = BASE_URL
weather_data = requests.get(final_url).json()
icon = weather_data.get("weather")[0].get("icon")
iconChopped = str(icon)[0] + str(icon)[1]
urlicon = f"http://openweathermap.org/img/wn/{icon}@2x.png"
currentTemp = str(weather_data.get("main").get("temp")) + "°C"
img = Image.open(f"weather_icons/{iconChopped}.png") 
img.show()


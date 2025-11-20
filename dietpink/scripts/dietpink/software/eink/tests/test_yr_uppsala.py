#!/usr/bin/env python3
import requests
import json

# Coordenades Uppsala
LAT = 59.8586
LON = 17.6389

# User-Agent (CANVIA el email!)
USER_AGENT = "dietpink/1.0 (github.com/Markuson; hi@marcuson.dev)"

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
params = {'lat': LAT, 'lon': LON}
headers = {'User-Agent': USER_AGENT}

print("🌤️  Test YR API per Uppsala...")
print(f"   Coordenades: ({LAT}, {LON})")
print("")

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    timeseries = data['properties']['timeseries'][0]
    
    # Next 6 hours
    if 'next_6_hours' in timeseries['data']:
        forecast = timeseries['data']['next_6_hours']
        symbol = forecast['summary']['symbol_code']
        precip = forecast['details'].get('precipitation_amount', 0)
        
        print("✅ Previsió pròximes 6 hores:")
        print(f"   Symbol: {symbol}")
        print(f"   Pluja: {precip} mm")
    
    # Temperatura actual
    temp = timeseries['data']['instant']['details']['air_temperature']
    print(f"   Temp actual: {temp}°C")
    print("")
    print("✅ YR API funciona!")
    
except Exception as e:
    print(f"❌ Error: {e}")

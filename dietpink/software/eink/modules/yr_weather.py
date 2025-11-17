#!/usr/bin/env python3
"""
yr_weather.py - Client per YR (met.no) Weather API
Obté previsió del temps per Uppsala
"""

import requests
from datetime import datetime, timedelta


class YRWeatherClient:
    """Client per obtenir previsió del temps de YR API"""
    
    def __init__(self, user_agent, lat=None, lon=None):
        """
        Inicialitzar client YR
        
        Args:
            user_agent: User-Agent string (obligatori per YR)
            lat: Latitud (opcional, es pot obtenir de HA)
            lon: Longitud (opcional, es pot obtenir de HA)
        """
        self.user_agent = user_agent
        self.lat = lat
        self.lon = lon
        self.last_forecast = None
        self.last_update = None
        
        self.api_url = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
    
    def set_coordinates(self, lat, lon):
        """Actualitzar coordenades"""
        self.lat = lat
        self.lon = lon
    
    def get_forecast(self):
        """
        Obtenir previsió del temps
        
        Returns:
            dict: {
                'symbol_code': str,
                'precipitation': float,
                'temperature': float,
                'timestamp': datetime,
                'success': bool
            }
        """
        if self.lat is None or self.lon is None:
            print("⚠️  YR: Coordenades no configurades")
            return self._empty_forecast()
        
        params = {
            'lat': self.lat,
            'lon': self.lon
        }
        
        headers = {
            'User-Agent': self.user_agent
        }
        
        try:
            print(f"🌤️  YR: Obtenint previsió per ({self.lat}, {self.lon})...")
            
            response = requests.get(
                self.api_url,
                params=params,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            forecast = self._parse_forecast(data)
            
            self.last_forecast = forecast
            self.last_update = datetime.now()
            
            print(f"   ✅ Symbol: {forecast['symbol_code']}")
            print(f"   ✅ Pluja: {forecast['precipitation']} mm")
            print(f"   ✅ Temp: {forecast['temperature']}°C")
            
            return forecast
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error cridant YR API: {e}")
            return self._empty_forecast()
        except Exception as e:
            print(f"   ❌ Error processant dades YR: {e}")
            return self._empty_forecast()
    
    def _parse_forecast(self, data):
        """Extreure dades rellevants de la resposta YR"""
        try:
            timeseries = data['properties']['timeseries']
            current = timeseries[0]
            
            # Instant data (temperatura actual)
            instant = current['data']['instant']['details']
            temperature = instant.get('air_temperature', 0)
            
            # Next 6 hours
            forecast_data = {
                'symbol_code': 'unknown',
                'precipitation': 0.0,
                'temperature': temperature,
                'timestamp': datetime.now(),
                'success': True
            }
            
            # Intentar obtenir next_6_hours
            if 'next_6_hours' in current['data']:
                next_6h = current['data']['next_6_hours']
                forecast_data['symbol_code'] = next_6h['summary']['symbol_code']
                forecast_data['precipitation'] = next_6h['details'].get('precipitation_amount', 0.0)
            
            # Fallback a next_1_hours si no hi ha next_6_hours
            elif 'next_1_hours' in current['data']:
                next_1h = current['data']['next_1_hours']
                forecast_data['symbol_code'] = next_1h['summary']['symbol_code']
                forecast_data['precipitation'] = next_1h['details'].get('precipitation_amount', 0.0)
            
            return forecast_data
            
        except (KeyError, IndexError) as e:
            print(f"   ⚠️  Error parseig YR: {e}")
            return self._empty_forecast()
    
    def _empty_forecast(self):
        """Retornar previsió buida en cas d'error"""
        return {
            'symbol_code': 'unknown',
            'precipitation': 0.0,
            'temperature': 0.0,
            'timestamp': datetime.now(),
            'success': False
        }
    
    def should_update(self, interval_hours=3):
        """
        Comprovar si cal actualitzar la previsió
        
        Args:
            interval_hours: Interval d'actualització en hores
            
        Returns:
            bool: True si cal actualitzar
        """
        if self.last_update is None:
            return True
        
        elapsed = datetime.now() - self.last_update
        return elapsed > timedelta(hours=interval_hours)
    
    def get_cached_forecast(self):
        """Obtenir última previsió en cache"""
        if self.last_forecast is None:
            return self._empty_forecast()
        return self.last_forecast


# Test del mòdul
if __name__ == "__main__":
    import json
    
    # Carregar config
    with open('../config/weather_config.json', 'r') as f:
        config = json.load(f)
    
    # Crear client
    client = YRWeatherClient(
        user_agent=config['yr_api']['user_agent'],
        lat=59.8586,  # Uppsala
        lon=17.6389
    )
    
    # Test
    forecast = client.get_forecast()
    print("\n📊 Resultat:")
    print(f"   Symbol: {forecast['symbol_code']}")
    print(f"   Pluja: {forecast['precipitation']} mm")
    print(f"   Temp: {forecast['temperature']}°C")
    print(f"   Success: {forecast['success']}")

import requests
from typing import Dict, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class WeatherModel:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, city: str, units: str = "metric") -> Optional[Dict]:
        """
        Obtiene los datos del clima para una ciudad específica.
        
        Args:
            city (str): Nombre de la ciudad
            units (str): Unidades de medida ('metric', 'imperial', 'standard')
            
        Returns:
            dict: Datos del clima formateados o None si hay un error
        """
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            
            data = response.json()
            return {
                "ciudad": city,
                "temperatura": data["main"]["temp"],
                "sensacion_termica": data["main"]["feels_like"],
                "humedad": data["main"]["humidity"],
                "descripcion": data["weather"][0]["description"],
                "viento": data["wind"]["speed"],
                "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except KeyError as key_err:
            print(f"Key error: {key_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    weather_model = WeatherModel()
    
    # Obtener el clima para diferentes ciudades
    cities = ["London", "Madrid", "Paris", "NonExistentCity"]
    
    for city in cities:
        weather_data = weather_model.get_weather(city)
        if weather_data:
            print(f"\nDatos del clima para {city}:")
            for key, value in weather_data.items():
                print(f"{key}: {value}")
        else:
            print(f"\nNo se pudo obtener datos para {city}")

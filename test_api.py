import requests
import json
from datetime import datetime
from typing import Dict, Optional, Union, List
import logging
from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class WeatherData:
    """Data class to store weather information"""
    city: str
    country: str
    temperature: float
    humidity: int
    wind_speed: float
    description: str
    pressure: int
    feels_like: float
    temp_min: float
    temp_max: float
    timestamp: datetime

class WeatherApiTester:
    """Class for testing the OpenWeatherMap API with enhanced features and error handling"""
    
    def __init__(self, api_key: Optional[str] = None, log_file: str = "weather_api_tests.log"):
        """
        Initialize the WeatherApiTester with API key and logging configuration
        
        Args:
            api_key (str, optional): OpenWeatherMap API key. If not provided, looks for OPENWEATHER_API_KEY env variable
            log_file (str): Path to log file
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY", "934bdc5186c2f332efd28b8369302ebd")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.setup_logging(log_file)
        self.results: List[WeatherData] = []
    
    def setup_logging(self, log_file: str) -> None:
        """Configure logging to both file and console"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def test_weather_api(self, city: str, units: str = "metric", save_to_file: bool = False) -> Optional[WeatherData]:
        """
        Test the weather API for a specific city
        
        Args:
            city (str): City name
            units (str): Units of measurement ('metric', 'imperial', 'standard')
            save_to_file (bool): Whether to save the response to a JSON file
            
        Returns:
            Optional[WeatherData]: Weather data if successful, None if failed
        """
        params = self._build_params(city, units)
        self.logger.info(f"Testing API for city: {city}")
        self.logger.debug(f"Request parameters: {json.dumps(params, indent=2)}")
        
        try:
            response = self._make_request(params)
            if response.status_code == 200:
                weather_data = self._process_success_response(response, city)
                if save_to_file:
                    self._save_response_to_file(city, response.json())
                return weather_data
            else:
                self._handle_error(response)
                return None
                
        except Exception as e:
            self._handle_exception(e)
            return None
    
    def _build_params(self, city: str, units: str) -> Dict[str, str]:
        """Build request parameters"""
        return {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
    
    def _make_request(self, params: Dict[str, str]) -> requests.Response:
        """Make HTTP request to the API"""
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        return response
    
    def _process_success_response(self, response: requests.Response, city: str) -> WeatherData:
        """Process successful API response"""
        data = response.json()
        weather_data = WeatherData(
            city=city,
            country=data.get('sys', {}).get('country', 'N/A'),
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
            description=data['weather'][0]['description'],
            pressure=data['main']['pressure'],
            feels_like=data['main']['feels_like'],
            temp_min=data['main']['temp_min'],
            temp_max=data['main']['temp_max'],
            timestamp=datetime.now()
        )
        self.results.append(weather_data)
        self._print_weather_data(weather_data)
        return weather_data
    
    def _print_weather_data(self, data: WeatherData) -> None:
        """Print weather data in a formatted way"""
        print("\n✅ Weather Data:")
        print("-" * 50)
        print(f"🌍 City: {data.city}, {data.country}")
        print(f"🌡️  Temperature: {data.temperature}°C (Feels like: {data.feels_like}°C)")
        print(f"📊 Min/Max: {data.temp_min}°C / {data.temp_max}°C")
        print(f"💧 Humidity: {data.humidity}%")
        print(f"🌪️  Wind Speed: {data.wind_speed} m/s")
        print(f"☁️  Weather: {data.description}")
        print(f"👥 Pressure: {data.pressure} hPa")
        print("-" * 50)
    
    def _save_response_to_file(self, city: str, data: Dict) -> None:
        """Save API response to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_data_{city}_{timestamp}.json"
        
        output_dir = Path("weather_data")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / filename, 'w') as f:
            json.dump(data, f, indent=2)
        self.logger.info(f"Saved response to {filename}")
    
    def _handle_error(self, response: requests.Response) -> None:
        """Handle API error responses"""
        error_messages = {
            401: "Authentication error. Please verify your API key.",
            404: "City not found.",
            429: "Too many requests. API limit exceeded.",
            500: "OpenWeatherMap server error.",
            503: "Service temporarily unavailable."
        }
        
        try:
            error_data = response.json()
            error_msg = (f"Error {response.status_code}: "
                        f"{error_messages.get(response.status_code, 'Unknown error')}. "
                        f"Details: {error_data.get('message', 'No details available')}")
            self.logger.error(error_msg)
        except:
            self.logger.error(f"Error {response.status_code}: "
                            f"{error_messages.get(response.status_code, 'Unknown error')}")
    
    def _handle_exception(self, e: Exception) -> None:
        """Handle general exceptions"""
        if isinstance(e, requests.exceptions.RequestException):
            self.logger.error(f"Connection error: {str(e)}")
        elif isinstance(e, json.JSONDecodeError):
            self.logger.error("Error decoding JSON response")
        else:
            self.logger.error(f"Unexpected error: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Union[float, int]]:
        """Calculate statistics from test results"""
        if not self.results:
            return {}
            
        temps = [r.temperature for r in self.results]
        return {
            "average_temperature": sum(temps) / len(temps),
            "max_temperature": max(temps),
            "min_temperature": min(temps),
            "total_cities_tested": len(self.results),
            "successful_tests": len([r for r in self.results if r.temperature is not None])
        }

def main():
    """Main function to run the tests"""
    tester = WeatherApiTester()
    
    cities = [
        "London",
        "Paris",
        "Madrid",
        "Tokyo",
        "NonExistentCity"
    ]
    
    print("🌍 Starting Weather API Tests...")
    for city in cities:
        tester.test_weather_api(city, save_to_file=True)
        print("\n" + "="*50 + "\n")
    
    # Print statistics
    stats = tester.get_statistics()
    if stats:
        print("\n📊 Test Statistics:")
        print("-" * 30)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")

if __name__ == "__main__":
    main()
#WeatherApp
import sys
import requests 
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout )
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter city name: ", self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather", self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)

        self.initUI()

    def initUI(self):
       self.setWindowTitle("Weather APP")

       Vbox = QVBoxLayout()
       Vbox.addWidget(self.city_label)
       Vbox.addWidget(self.city_input)
       Vbox.addWidget(self.get_weather_button)
       Vbox.addWidget(self.temperature_label)
       Vbox.addWidget(self.emoji_label)
       Vbox.addWidget(self.description_label)

       self.setLayout(Vbox)
       
       self.city_label.setAlignment(Qt.AlignCenter)
       self.city_input.setAlignment(Qt.AlignCenter)
       self.temperature_label.setAlignment(Qt.AlignCenter)
       self.emoji_label.setAlignment(Qt.AlignCenter)
       self.description_label.setAlignment(Qt.AlignCenter)

       self.city_label.setObjectName("City_label")
       self.city_input.setObjectName("City_input")
       self.get_weather_button.setObjectName("Get_weather_button")
       self.temperature_label.setObjectName("Temperature_label")
       self.emoji_label.setObjectName("Emoji_label")
       self.description_label.setObjectName("Description_label")

       self.setStyleSheet("""
                QLabel, QPushButton{
                        font-family: Calibri;
                     }
                QLabel#City_label{
                        font-size: 40px;
                        font-weight: Bold;   
                          }
                QLineEdit#City_input{
                        font-size: 40px;
                          padding: 8px;
                          }
                QPushButton#Get_weather_button{
                          font-size: 30px;
                          }
                QLabel#Temperature_label{
                          font-size: 75px;
                          }
                QLabel#Emoji_label{
                          font-size: 75px;
                          font-family: Apple Color Emoji !important;
                          }
                QLabel#Description_label{
                          font-size: 50px;
                          }
        """)
       self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "349ede72de054ee61150182c7733acdb"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
           response = requests.get(url)
           response.raise_for_status()
           data = response.json()
           if data["cod"] == 200:
              self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
           match http_error.response.status_code:
              case 400:
                 self.display_error("Bad Request\nPlease check your input.")
              case 401:
                 self.display_error("Unauthorized\nInvalid API key.")
              case 403:
                 self.display_error("Forbidden\nAccess is denied")
              case 404:
                 self.display_error("Not found\nCity not found.")
              case 500:
                 self.display_error("Internal server error\nPlease try again later.")
              case 502:
                 self.display_error("Bad gateway\nInvalid response from the server.")
              case 503:
                 self.display_error("Service unavailable\nServer is down.")
              case 504:
                 self.display_error("Gateway timeout\nNo response from the server.")
              case _:
                 self.display_error(f"HTTP error\n{http_error}")

        except requests.exceptions.ConnectionError:
           self.display_error("Connection Error:\nCheck you internet connection.")
        except requests.exceptions.Timeout:
           self.display_error("Timeout Error:\nThe request timeout.")
        except requests.exceptions.TooManyRedirects:
           self.display_error("Too Many Redirections\nCheck the URL.")
        except requests.exceptions.RequestException as req_error:
           self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
       self.temperature_label.setStyleSheet("font-size: 30px;")
       self.temperature_label.setText(message)
       self.emoji_label.clear()
       self.description_label.clear()
    def display_weather(self, data):
       self.temperature_label.setStyleSheet("font-size: 75px")
       temperature_c = data["main"]["temp"]
       weather_id = data["weather"][0]["id"]
       weather_description = data["weather"][0]["description"]
       self.temperature_label.setText(f"{temperature_c:.0f}°C")
       self.emoji_label.setText(self.get_weather_emoji(weather_id))
       self.description_label.setText(weather_description)
    @staticmethod
    def get_weather_emoji(weather_id):
       if 200 <= weather_id <= 232:
          return "⛈️"
       elif 300 <= weather_id <= 321:
          return "🌦️"
       elif 500 <= weather_id <= 521:
          return "🌧️"
       elif 600 <= weather_id <= 622:
          return "❄️"
       elif 701 <= weather_id <= 741:
          return "🌫️"
       elif weather_id == 762:
          return "🌋"
       elif weather_id == 771:
          return "🌬️"
       elif weather_id == 781:
          return "🌪️"
       elif weather_id == 800:
          return "☀️"
       elif 801 <= weather_id <= 804:
          return "☁️"
       else:
          return " "
       
if __name__=="__main__":
 app = QApplication(sys.argv)
 weather_app = WeatherApp()
 weather_app.show()
 sys.exit(app.exec_())

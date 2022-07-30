import os
import csv
from datetime import datetime
from collections import defaultdict
from sty import fg


class ReadWheatherFiles:
    path = "/Users/ahsan/Desktop/ArbiSoft/Tasks/weatherman/weatherfiles"
    files_weather_data = {}

    def reading_weather_files(self):
        files_path = self.path
        input_data = self.files_weather_data
        weather_files = os.listdir(files_path)
        for file in weather_files:
            if os.path.isfile(os.path.join(files_path, file)):
                with open(os.path.join(files_path, file), 'r') as weather_reader:
                    read_line = weather_reader.readlines()
                    weather_obj = csv.DictReader(read_line)
                    for row in weather_obj:
                        if row.get('PKT'):
                            date = datetime.strptime(str(row['PKT']), "%Y-%m-%d")
                        elif row.get('PKST'):
                            date = datetime.strptime(str(row['PKST']), "%Y-%m-%d")
                        input_data.setdefault(date.year, {}).setdefault(date.month, []).append(row)
                weather_reader.close()


class WeatherCalculations:

    def __init__(self, weather_data, userinput):
        self.weather_data = weather_data
        self.userinput = userinput

    def weather_calculations(self):
        weather_reader = self.weather_data
        userinput = self.userinput

        param_user_input = userinput[0:2]
        rem_user_input = userinput[2:]
        key_user_input = str(rem_user_input).strip()
        key_user_year = 0
        key_user_month = 0
        if param_user_input == '-a':
            key_user_year = key_user_input
        elif param_user_input == '-e':
            split_user_input_key = key_user_input.split('/')
            key_user_year = split_user_input_key[0]
            key_user_month = split_user_input_key[1]
        elif param_user_input == '-c':
            split_user_input_key = key_user_input.split('/')
            key_user_year = split_user_input_key[0]
            key_user_month = split_user_input_key[1].lstrip('0')

        for key_year, year in weather_reader.items():
            if key_year == int(key_user_year):
                for key_month, month in year.items():
                    if key_month == int(key_user_month):
                        monthly_bar_chart_data = list(month)
                        weather_dict = WeatherCalculations.filter_weather(month, key_year)
                        break
                    elif key_user_month == 0:
                        weather_dict = WeatherCalculations.filter_weather(month, key_year)

                min_temp = weather_dict['min_temp']
                max_temp = weather_dict['max_temp']
                max_humidity = weather_dict['max_humidity']
                min_humidity = weather_dict['min_humidity']

        max_temp = WeatherCalculations.find_max(max_temp, 'Max TemperatureC')
        min_temp = WeatherCalculations.find_min(min_temp, 'Min TemperatureC')
        max_humidity = WeatherCalculations.find_max(max_humidity, 'Max Humidity')
        min_humidity = WeatherCalculations.find_min(min_humidity, ' Min Humidity')

        if param_user_input == str('-a') or\
                param_user_input == str('-e'):
            output_data = WeatherCalculations.create_output(max_temp, min_temp, max_humidity, min_humidity)
            WeatherCalculations.find_min_max(output_data)
        elif param_user_input == str('-c'):
            WeatherCalculations.draw_chart_temp(monthly_bar_chart_data)

    """
     Arrange Minimum and Maximum Tempreture and Humidity for Result
    """
    @staticmethod
    def find_min_max(output_data):
        for key_year, year in output_data.items():
            if year[0].get('PKT'):
                get_date = year[0].get('PKT')
            else:
                get_date = year[0].get('PKST')
            max_t = year[0].get('Max TemperatureC')
            max_t_date = datetime.strptime(get_date, '%Y-%m-%d').date()
            if year[1].get('PKT'):
                get_date = year[1].get('PKT')
            else:
                get_date = year[1].get('PKST')
            min_t = year[1].get('Min TemperatureC')
            min_t_date = datetime.strptime(get_date, '%Y-%m-%d').date()
            if year[1].get('PKT'):
                get_date = year[1].get('PKT')
            else:
                get_date = year[1].get('PKST')
            max_hum = year[2].get('Max Humidity')
            max_hum_date = datetime.strptime(get_date, '%Y-%m-%d').date()
            if year[1].get('PKT'):
                get_date = year[1].get('PKT')
            else:
                get_date = year[1].get('PKST')
            min_hum = year[3].get(' Min Humidity')
            min_hum_date = datetime.strptime(get_date, '%Y-%m-%d').date()

            print('Highest Tempreture: ',
                  max_t, 'C', 'on',
                  max_t_date.strftime("%B"),
                  max_t_date.strftime("%d"),
                  max_t_date.strftime("%Y"))
            print('Lowest Tempreture: ',
                  min_t, 'C', 'on',
                  min_t_date.strftime("%B"),
                  min_t_date.strftime("%d"),
                  min_t_date.strftime("%Y"))
            print('Highest Humidity: ',
                  max_hum, 'C', 'on',
                  max_hum_date.strftime("%B"),
                  max_hum_date.strftime("%d"),
                  max_hum_date.strftime("%Y"))
            print('Lowest Humidity: ',
                  min_hum, 'C', 'on',
                  min_hum_date.strftime("%B"),
                  min_hum_date.strftime("%d"),
                  min_hum_date.strftime("%Y"))
            print('---------------------------------------------------------------')

    """
     Draw Horizontal Bar Chart on the base of maximum
     and minimum Tempreture. Blue Chart shows min tempreture
     and Red Chart shows max tempreture from the given data
    """
    @staticmethod
    def draw_chart_temp(output_data):
        for mon_day in output_data:
            if mon_day.get('PKT'):
                get_date = mon_day.get('PKT')
            else:
                get_date = mon_day.get('PKST')
            mon_date = str(get_date[-2:]).lstrip('-')

            if mon_day['Max TemperatureC'] != '':
                print(fg.magenta + mon_date + fg.rs, end=" ")
                for val in range(int(mon_day['Max TemperatureC'])):
                    print(fg.red + "+" + fg.rs, end="")
                print("", fg.magenta + mon_day['Max TemperatureC'] + "C" + fg.rs, end="\n")
            if mon_day['Min TemperatureC'] != '':
                print(fg.magenta + mon_date + fg.rs, end=" ")
                for val in range(int(mon_day['Min TemperatureC'])):
                    print(fg.blue + "+" + fg.rs, end="")
                print("", fg.magenta + mon_day['Min TemperatureC'] + "C" + fg.rs, end="\n")

        print('------------------------------------------------')

    """ 
        Find Minimum Tempreture and Humidity from the given dictionary.
        After filteration store in new dictionary
    """

    @staticmethod
    def find_min(input_dict, key):
        out_dict = {}
        for key_year, year in input_dict.items():
            clean_list = WeatherCalculations.clean(year, key)
            if clean_list:
                minimum = min(clean_list, key=lambda x: int(x[key]))
                out_dict[key_year] = minimum
            else:
                out_dict[key_year] = {}

        return out_dict

    """ 
        Find Maximum Tempreture and Humidity from the given dictionary.
        After filteration store in new dictionary
    """

    @staticmethod
    def find_max(input_dict, key):
        out_dict = {}
        for key_year, year in input_dict.items():
            clean_list = WeatherCalculations.clean(year, key)
            if clean_list:
                maximum = max(clean_list,  key=lambda x: int(x[key]))
                out_dict[key_year] = maximum
            else:
                out_dict[key_year] = {}
        return out_dict

    """
        Clean Dict from empty values and return new List
    """

    @staticmethod
    def clean(length, key):
        new_list = []
        for d in length:
            value = d.get(key)
            if value != '':
                new_list.append(d)
        return new_list

    """
        Take Multiple dicts and return Single List which 
        contain Max and Min Tempreture, Humidity values
    """

    @staticmethod
    def create_output(*dicts):
        output_data = defaultdict(list)
        for d in dicts:
            for key, value in d.items():
                output_data[key].append(value)
        return output_data

    """
        Take All Weather data and apply filteration on it and return
        filtered dictionary
    """

    @staticmethod
    def filter_weather(month, key_year):
        min_temp = {}
        max_temp = {}
        max_humidity = {}
        min_humidity = {}

        min_temp_list = []
        max_temp_list = []
        min_humidity_list = []
        max_humidity_list = []

        min_temp_list.append(min(month, key=lambda x: x['Min TemperatureC']))
        min_temp[key_year] = min_temp_list
        max_temp_list.append(max(month, key=lambda x: x['Max TemperatureC']))
        max_temp[key_year] = max_temp_list
        max_humidity_list.append(max(month, key=lambda x: x['Max Humidity']))
        max_humidity[key_year] = max_humidity_list
        min_humidity_list.append(min(month, key=lambda x: x[' Min Humidity']))
        min_humidity[key_year] = min_humidity_list

        return dict(min_temp=min_temp,
                    max_temp=max_temp,
                    max_humidity=max_humidity,
                    min_humidity=min_humidity)


if __name__ == '__main__':
    files_read = ReadWheatherFiles()
    files_read.reading_weather_files()
    weather_data = files_read.files_weather_data

    userinput = input("")
    reading_cal = WeatherCalculations(weather_data, userinput)
    reading_cal.weather_calculations()


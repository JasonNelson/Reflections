# Reflections - Changes the look and feel of the MacOS environment
# to reflect things like the weather, your mood and many other inputs.
# Copyright (C) 2017 Jason Nelson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from urllib import request
import re
import json

from wallpaper import *

# gets current weather conditions and sun phase times from WU
def getWeather(city, zipcode):

    inFile = "https://www.wunderground.com/weather/us/wa/" + city + "/" + zipcode
    json_file = request.urlopen(inFile) # read html file into string
    raw_string = json_file.read().decode('utf-8') # decode string
    json_regex = "(<script>window\['UNIVERSAL_CACHE'\] = )(.*?)(</script>)"
    json_string = re.search(json_regex,raw_string).group(2) #extract actual json from string

    if json_string:
        # get first key value
        key1_regex = '{"([\d\w]*)":{'
        key1 = re.search(key1_regex, json_string).group(1)

        key2_regex = '=JSONP_CALLBACK"},"([\d\w]*)":'
        key2 = re.search(key2_regex, json_string).group(1)

        # convert json string to dict
        parsed_json = json.loads(json_string)

        if (key1 and key2):
            # compile regex pattern for times
            time_regex = '(\d{2}):(\d{2}):\d{2}'
            time_pattern = re.compile(time_regex)

            # get current time as minutes past midnight
            currentTime = parsed_json[key1]['value']['response']['date']['iso8601']
            current_hr = re.search(time_pattern, currentTime).group(1)
            current_min = re.search(time_pattern, currentTime).group(2)
            currentTime = (int(current_hr) * 60) + int(current_min)

            # get current condition key  [note: _12char and _32char also available]
            conditionKey = parsed_json[key2]['value']['observation']['phrase_22char']

            # get time of sunrise and sunset as minutes past midnight
            sunrise, sunset = parsed_json[key2]['value']['observation']['sunrise'], parsed_json[key2]['value']['observation']['sunset']

            sunrise_hr = re.search(time_pattern, sunrise).group(1)
            sunrise_min = re.search(time_pattern, sunrise).group(2)
            sunrise = (int(sunrise_hr) * 60) + int(sunrise_min)

            sunset_hr = re.search(time_pattern, sunset).group(1)
            sunset_min = re.search(time_pattern, sunset).group(2)
            sunset = (int(sunset_hr) * 60) + int(sunset_min)

            # determine whether it is currently day or night
            timeOfDay = "day " if (currentTime >= sunrise and currentTime < sunset) else "night "
            json_file.close()
            return str(timeOfDay) + conditionKey.lower() + " wallpaper"

def main():

    wallpaperPath = <path to save wallpapers to>   # must end in '/'
    numberResults = 5     # number of wallpaper urls to retrieve
    imageSize = 'huge'    # size of wallpaper (use: small, medium, large, xlarge, xxlarge, huge)
    city  = <your city here>
    zipcode = <your zipcode here>

    # set wallpaper
    setWallpaper(getWeather(city, zipcode), wallpaperPath, numberResults, imageSize)

if __name__ == '__main__':
    main()

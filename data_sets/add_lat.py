import json, csv
import urllib.request, urllib.parse

MAPS_API_KEY = 'AIzaSyAN7INNbgTIVwUR1bhKSH3Dml0DRUck6mY'
CSV_FILE_NAME = 'edu.csv'

def get_lat_long(place):
    place_search_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    place_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json?'
    get_place_params = {
        'key': MAPS_API_KEY,
        'inputtype': 'textquery',
        'input' : place
    }
    get_place_url = place_search_url + urllib.parse.urlencode(get_place_params)
    with urllib.request.urlopen(get_place_url) as response:
        data = json.load(response)
        place_id = data['candidates'][0]['place_id']

    get_geo_params = {
        'key': MAPS_API_KEY,
        'fields' : 'geometry',
        'placeid': place_id
    }
    get_geo_url = place_detail_url + urllib.parse.urlencode(get_geo_params)
    with urllib.request.urlopen(get_geo_url) as response:
        data = json.load(response)
        loc = data['result']['geometry']['location']
    return (loc['lat'], loc['lng'])


csv_source = open(CSV_FILE_NAME, 'r', encoding='utf-8')
csv_reader = csv.reader(csv_source)

csv_dest = open('dest.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_dest)

i=0
for line in csv_reader:
    if len(line) == 0:
        continue
    flag = 0
    for field in line:
        if field == '':
            flag = 1
            break
    if flag == 1:
        continue
    if i:  
        loc = get_lat_long(f'{line[3]}, {line[2]}')
        line[0] = loc[0]
        line[1] = loc[1]
    line[2] = line[2].title()
    line[3] = line[3].title()
    csv_writer.writerow(line)
    print(f'added {line[3]}')
    i += 1

csv_dest.close()
csv_source.close()

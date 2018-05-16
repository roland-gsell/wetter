import requests
import bs4
import collections


city = collections.namedtuple('cities',
                              'name, link')
wetter_status = collections.namedtuple('wetter_status',
                                       'temp, status, zeit')


def main():
    print_header()
    plz = True
    while plz:
        plz = input('Welche Postleitzahl? (Enter = Ende) ')
        if plz:
            html = get_search_result_html(plz)
            cities = get_cities(html)
            for count, city in enumerate(cities):
                print(count + 1, city.name)
            city_number = int(input('Welche Stadt willst du? '))
            chosen_city_link = cities[city_number - 1].link
            print('Link: ', chosen_city_link)
            wetter_html = get_weather_html(chosen_city_link)
            wetter = get_weather(wetter_html)
            print(wetter.zeit, wetter.temp, wetter.status)


def get_weather(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    temperatur = soup.find(class_='temp').text
    status = soup.find(class_='icontext').text
    titel = soup.find(class_='title').text
    wetter = wetter_status(temp=temperatur, status=status, zeit=titel)
    return wetter


def get_cities(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    city_list = []
    for entry in soup.find(class_='entrys').find_all('a', href=True):
        c = city(name=entry.text.strip(), link=entry['href'])
        city_list.append(c)
    return city_list


def get_weather_html(city_link):
    response = requests.get(city_link)
    return response.text


def get_search_result_html(plz):
    response = requests.get('http://www.wetter.at/locationSearch/' + plz)
    return response.text


def print_header():
    print('-----------------------------')
    print('         Wetter-App')
    print('-----------------------------')
    print()


if __name__ == '__main__':
    main()
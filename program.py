import requests
import bs4
import collections


city = collections.namedtuple('cities',
                              'name, link')


def main():
    print_header()
    html = get_search_result_html()
    cities = get_cities(html)
    for count, city in enumerate(cities):
        print(count + 1, city.name)
    city_number = int(input('Which one do you want? '))
    print(cities[city_number - 1].link)


def get_cities(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    city_list = []
    for entry in soup.find(class_='entrys').find_all('a', href=True):
        c = city(name=entry.text.strip(), link=entry['href'])
        city_list.append(c)
    return city_list


def get_search_result_html():
    response = requests.get('http://www.wetter.at/locationSearch/3500')
    return response.text


def print_header():
    print('-----------------------------')
    print('         Wetter-App')
    print('-----------------------------')
    print()


if __name__ == '__main__':
    main()
import requests
import fake_useragent
from bs4 import BeautifulSoup

while True:
    try:
        #получение правильного имени героя 
        wrong_hero = input('Введите имя нужного героя:   ').strip()
        correct_hero = '-'.join(wrong_hero.strip().lower().split())

        #ссылка на страницу
        link = f'https://ru.dotabuff.com/heroes/{correct_hero}/counters'
        #создание фейкового юзер агента
        user = fake_useragent.UserAgent().random

        #хедер с фейковым юзер агентом
        header = {
            'user-agent': user
        }

        #запрос на код страницы
        response = requests.get(link, headers = header)

        #обработка ошибки 404(сервер не отвечает или не найден)
        if response.status_code == 404:
            print('Некорректное имя героя, введите правильное')
        else:
            #переменная которая хранит код страницы тексом
            soup = BeautifulSoup(response.text, 'lxml')

            #искать секцию
            section = soup.find('section', class_='counter-outline')
            #искать ВСЕ СТРОКИ
            rows = section.find_all('tr')

            for row in rows[:5]:
                #искать секции в ОДНОЙ СТРОКЕ
                tds = row.find_all('td')
                if len(tds) >= 3:
                    name = tds[1].text.strip()
                    opposition = tds[2].text.strip()
                    print(f'{name}: {opposition}')
                    
    except KeyboardInterrupt:
        print('\nПрограмма закрыта')
        break
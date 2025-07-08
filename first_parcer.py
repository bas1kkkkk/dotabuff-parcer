import asyncio
import aiohttp
import fake_useragent
from bs4 import BeautifulSoup
from collections import defaultdict

async def fetch_counters(session, hero, all_counters):
    user = fake_useragent.UserAgent().random
    headers = {'user-agent': user}
    url = f'https://ru.dotabuff.com/heroes/{hero}/counters'

    async with session.get(url, headers=headers) as response:
        if response.status == 404:
            print(f'Некорректное имя героя: {hero}')
            return

        text = await response.text()
        soup = BeautifulSoup(text, 'lxml')
        table = soup.find('table', class_='sortable')
        if not table:
            print(f'Не найдена таблица контрпиков для {hero}')
            return
        
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        
        print(f'\nКонтрпики для {hero.capitalize()}:')
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 3:
                name = tds[1].text.strip()
                opposition_str = tds[2].text.strip().replace('%', '').replace(',', '')
                try:
                    opposition = float(opposition_str)
                    if opposition > 0:
                        print(f'{name}: {opposition}%')
                        all_counters[name][hero] = opposition
                except ValueError:
                    continue
        print()

async def main():
    while True:
        try:
            wrong_heroes = input('Введите имена нужных героев: ').strip().split(',')
            correct_heroes = ['-'.join(hero.lower().split()) for hero in wrong_heroes]

            all_counters = defaultdict(dict)

            async with aiohttp.ClientSession() as session:
                tasks = [fetch_counters(session, hero, all_counters) for hero in correct_heroes]
                await asyncio.gather(*tasks)

            # Показать топ-5 только если больше одного героя
            if len(correct_heroes) > 1:
                common_counters = {
                    hero: sum(values.values())
                    for hero, values in all_counters.items()
                    if len(values) == len(correct_heroes)
                }

                top_5 = sorted(common_counters.items(), key=lambda x: x[1], reverse=True)[:5]

                print('\nТОП-5 контрпиков против всех выбранных героев:')
                for name, total in top_5:
                    avg = total / len(correct_heroes)
                    print(f'{name}: {avg:.2f}% в среднем')

        except KeyboardInterrupt:
            print('\nПрограмма закрыта')
            break

if __name__ == '__main__':
    asyncio.run(main())

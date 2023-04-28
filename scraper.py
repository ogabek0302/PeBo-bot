import requests
from bs4 import BeautifulSoup


def get_product_prices(product_name):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    urls = {
        'Amazon': f'https://www.amazon.com/s?k={product_name}',
        'eBay': f'https://www.ebay.com/sch/i.html?_nkw={product_name}',
        'Walmart': f'https://www.walmart.com/search/?query={product_name}',
        'Uzum': f'https://uzum.uz/ru/search?query={product_name}',
        'Aliexpress': f'https://aliexpress.ru/wholesale?SearchText={product_name}',
        'Yandex': f'https://market.yandex.ru/search?cvredirect=1&text={product_name}'
     }
# https://aliexpress.com - https://aliexpress.ru/wholesale?SearchText=
# https://uzum.uz/ - https://uzum.uz/ru/search?query=
# https://market.yandex.ru/ - https://market.yandex.ru/search?cvredirect=1&text=

    prices = {}
    for site, url in urls.items():
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        if site == 'Amazon':
            price = soup.find('span', {'class': 'a-offscreen'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '
        elif site == 'eBay':
            price = soup.find('span', {'class': 's-item__price'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '
        elif site == 'Walmart':
            price = soup.find('span', {'class': 'price-main'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '
        elif site == 'Uzum':
            price = soup.find('span', {'class': 'currency product-card-price slightly medium'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '
        elif site == 'Yandex':
            price = soup.find('data-baobab-name', {'class': 'price'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '
        elif site == 'Aliexpress':
            price = soup.find('div', {'class': 'snow-price_SnowPrice__mainM__azqpin'})
            if price:
                prices[site] = price.text
            else:
                prices[site] = 'topilmadi '        
    return prices

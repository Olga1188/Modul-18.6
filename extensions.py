
import requests
import json      #библиотека json ля парсинга полученных ответов
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]  # если неправильно введена конвертируемая валюта
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base] # если неправильно введена базовая валюта
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount) #если сумма не число
        except ValueError:
            raise APIException(f'Не удалось обработать колличество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}') #отправляем запрос
        total_base = json.loads(r.content)[keys[base]]  #ответ кладем в переменную
        # print(round(total_base * float(amount), 2))
        return round(total_base * float(amount), 2)  #возаращаем сумму
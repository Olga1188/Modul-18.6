
import telebot
from config import TOKEN, keys
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # При вводе команды /start или /help пользователю выводятся инструкции по применению бота
def help(message: telebot.types.Message):
    text = 'Для конвертации валюты введите команду боту в формате: \n  <валюта которую отдаем> <валюта которую получаем> <сумма>' \
           '\n <Пример:  доллар рубль 100> \n Список доступных валют: /values \n Помощь /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=[
    'values'])  # При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')  # преобразуем сообщение в список
        if len(values) != 3:  # если список != 3 элементам
            raise APIException('Некорректный ввод')

        quote, base, amount  = values  # присваиваем переменные каждому элементу списка
        total_base = CryptoConverter.convert(quote.lower(), base.lower(),
                                             amount)  # вызываем метод convert класса CryptoConverter
    except APIException as e:  # ловим ошибки пользователя
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:  # Ловим ошибки сервера
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        # print(total_base)
        text = f'За {amount} {quote} вы получите \n {total_base} {base}'  # считаем сумму и округляем до 4го знака после запятой
        bot.send_message(message.chat.id, text)  # передаем сообщение с суммой сконвертируемой валюты


bot.polling(none_stop=True)
import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Здесь плохочитаемая запись переноса.
        # Лучше оставить if not date на второй строке.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменная названа с большой буквы, как класс. Нужно просто record.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # today - record.date вычисляется дважды.
            # Лучше вынести в отдельную переменную
            # или сравнить как if 0 <= (today - record.date).days < 7
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Нужно избегать бэкслешей для переноса.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # USD_RATE = 60.0 пишется короче и читается лучше.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Параметры USD_RATE, EURO_RATE в методе избыточны и только запутывают код.
    # Курсы уже определены как атрибуты класса self.USD_RATE и self.EURO_RATE.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Следующая строка лишняя и вносит путаницу.
        # currency - параметр с возможными значениями 'usd', 'eur', 'rub'.
        # currency_type - переменная для формирования ответа с возможными
        # значениями 'USD', 'Euro', 'руб'.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        # Нужно проверять currency
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # Здесь можно обойтись else. А лучше вообще убрать и в начале до if'ов
        # сделать дефолтный вариант для рублей. Так будет проще добавлять
        # новые валюты в будущем.
        elif currency_type == 'rub':
            # Следующая строка с ошибкой, так как должен быть /=, а не ==.
            # Но лучше вообще убрать, так как не нужно пересчитывать рубли.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Здесь не нужно разделять строку на несколько.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Это условие можно не писать, так как в предыдущих был return
        elif cash_remained < 0:
            # Лучше использовать f-строки. И избегать \ для переноса.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Метод просто вызывает родительский метод, не добавляя никакой логики.
    # Это делает его полностью избыточным. Метод и так наследуется 
    # от родительского класса.
    def get_week_stats(self):
        super().get_week_stats()


# Вот такое можно написать для проверки
if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
        
    cash_calculator.add_record(Record(amount=145, comment='кофе')) 
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(
        Record(amount=3000, comment='бар в Танин др', date='08.11.2019'))
                    
    print(cash_calculator.get_today_cash_remained('rub'))

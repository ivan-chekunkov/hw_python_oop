import datetime as dt


class Calculator:
    """Родительский класс для калькуляторов."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        """Добавление записи данных в калькулятор."""

        self.records.append(rec)

    def get_today_stats(self):
        """Возвращает статистику за день."""

        day_sum = 0
        now = dt.datetime.now().date()
        for record in self.records:
            if record.date == now:
                day_sum += record.amount
        return day_sum

    def get_week_stats(self):
        """Возвращает статистику за неделю."""

        week_sum = 0
        date_now = dt.datetime.now().date()
        date_delta = date_now - dt.timedelta(weeks=1)
        for record in self.records:
            date_record = record.date
            if date_delta < date_record <= date_now:
                week_sum += record.amount
        return week_sum

    def get_cash_remained(self):
        """Возвращает остаток от лимита."""

        return self.limit - self.get_today_stats()


class Record:
    """Класс записи данных в калькулятор."""

    FORMAT_DATE = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.FORMAT_DATE).date()


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self):
        """Возвращает статус разрешённых калорий на сегодняшний день."""

        cal_day_remained = self.get_cash_remained()
        if cal_day_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{cal_day_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег."""

    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """Возвращает статус оставшихся денег на сегодняшний день."""

        all_currency: dict = {
            'rub': (self.RUB_RATE, 'руб'),
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD')
        }
        sum_day_remained = self.get_cash_remained()
        if sum_day_remained == 0:
            return 'Денег нет, держись'

        out = abs(sum_day_remained / all_currency[currency][0])
        currency_type = all_currency[currency][1]
        if sum_day_remained > 0:
            return f'На сегодня осталось {out:.2f} {currency_type}'
        return (f'Денег нет, держись: твой долг - {out:.2f} '
                f'{currency_type}')

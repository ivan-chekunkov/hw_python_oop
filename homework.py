import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        self.records.append(rec)

    def get_today_stats(self):
        day_sum = 0
        now = dt.datetime.now().date()
        for record in self.records:
            if record.date == now:
                day_sum += record.amount
        return day_sum

    def get_week_stats(self):
        week_sum = 0
        date_now = dt.datetime.now().date()
        date_delta = date_now - dt.timedelta(weeks=1)
        for record in self.records:
            date_record = record.date
            if date_delta < date_record <= date_now:
                week_sum += record.amount
        return week_sum

    def get_cash_remained(self):
        return self.limit - self.get_today_stats()


class Record:
    FORMAT_DATE = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, self.FORMAT_DATE).date()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        cal_day_accumulated = self.get_today_stats()
        if cal_day_accumulated < self.limit:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.get_cash_remained()} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 70.00
    EURO_RATE = 80.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        sum_day_spent = self.get_today_stats()
        if sum_day_spent == self.limit:
            return 'Денег нет, держись'
        all_currency: dict = {
            'rub': (self.RUB_RATE, 'руб'),
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD')
        }
        out = abs(self.get_cash_remained() / all_currency[currency][0])
        currency_type = all_currency[currency][1]
        if sum_day_spent < self.limit:
            return f'На сегодня осталось {out:.2f} {currency_type}'
        return (f'Денег нет, держись: твой долг - {out:.2f} '
                f'{currency_type}')

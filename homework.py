import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = list()

    def add_record(self, rec):
        self.records.append(rec)

    def get_today_stats(self):
        day_summa = 0
        now = dt.datetime.now().date()
        for i in self.records:
            if i.date == now:
                day_summa += i.amountgi
        return day_summa

    def get_week_stats(self):
        week_summa = 0
        date = dt.datetime.now() - dt.timedelta(weeks=1)
        for i in self.records:
            if i.date > date.date() and i.date <= dt.datetime.now().date():
                week_summa += i.amount
        return week_summa


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(
            date, '%d.%m.%Y').date() if date else dt.datetime.now().date()


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        cal_day_accumulated = 0
        now = dt.datetime.now().date()
        for i in self.records:
            if i.date == now:
                cal_day_accumulated += i.amount
        if cal_day_accumulated < self.limit:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{self.limit-cal_day_accumulated} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 70.00
    EURO_RATE = 80.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        all_currency: dict = {
            'rub': (self.RUB_RATE, 'руб'),
            'eur': (self.EURO_RATE, 'Euro'),
            'usd': (self.USD_RATE, 'USD')
        }
        sum_day_spent = 0
        now = dt.datetime.now().date()
        for i in self.records:
            if i.date == now:
                sum_day_spent += i.amount
        out = abs((self.limit - sum_day_spent) / all_currency[currency][0])
        if sum_day_spent == self.limit:
            return 'Денег нет, держись'
        elif sum_day_spent < self.limit:
            return f'На сегодня осталось {out:.2f} {all_currency[currency][1]}'
        else:
            return (f'Денег нет, держись: твой долг - {out:.2f} '
                    f'{all_currency[currency][1]}')

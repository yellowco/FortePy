class Recurrence(object):
    WEEKLY = 10
    BIWEEKLY = 15
    MONTHLY = 20
    BIMONTHY = 25
    QUARTERLY = 30
    SEMIANNUALY = 35
    YEARLY = 40
    def __init__(self, quantity, frequency, amount=None, start_date=None):
        self.quantity = quantity
        self.frequency = frequency
        self.amount = amount
        self.start_date = start_data

    @property
    def data(self):
        data = {'pg_schedule_quantity':self.quantity,
                'pg_schedule_frequency':self.frequency,
                'pg_schedule_recurring_amount':self.amount}
        if self.start_date:
            data['pg_schedule_start_date'] = self.start_date.strftime("%d/%m/%Y")
        return data

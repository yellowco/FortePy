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

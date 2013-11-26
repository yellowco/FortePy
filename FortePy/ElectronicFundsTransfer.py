import RetrospectiveTransaction

class ElectronicFundsTransfer(RetrospectiveTransaction.RetrospectiveTransaction):
    SAVINGS = "S"
    CHECKING = "C"
    def __init__(self, routing_number, account_number, account_type):
        super().__init__(None, None)
        self.routing_number = routing_number
        self.account_number = account_number
        self.account_type = account_type

    @property
    def data(self):
        return {'ecom_payment_check_trn': self.routing_number,
                'ecom_payment_check_account': self.account_number,
                'ecom_payment_check_account_type': self.account_type}

    def sale(self, amount):
        return self.transaction(20, amount)

    def authorization(self, amount):
        return self.transaction(21, amount)

    def capture(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(22, amount)

    def credit(self, amount):
        return self.transaction(23, amount)

    def void(self, amount):
        if self.trace_number is None:
            raise AttributeError("Original trace number not set")
        return self.transaction(24, amount)

    def force(self, amount):
        return self.transaction(25, amount)

    def verify(self, amount):
        return self.transaction(26, amount)
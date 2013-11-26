class RetrospectiveTransaction(object):
    def __init__(self, trace_number=None, authorization_code=None):
        self.trace_number = trace_number
        self.authorization_code = authorization_code

    def using(self, trace_number, authorization_code):
        self.trace_number = trace_number
        self.authorization_code = authorization_code

    @property
    def data(self):
        return {}

    def transaction(self, type, amount):
        d = {'pg_transaction_type': type,
             'pg_total_amount': amount,
             'pg_original_trace_number': self.trace_number,
             'pg_original_authorization_code': self.authorization_code}
        d.update(self.data)
        return d


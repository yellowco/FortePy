import DirectSocketInterface

class Forte(object):
    def __init__(self, hostname='www.paymentsgateway.net', port=6050, merchant_id=None, password=None):
        self.socket = DirectSocketInterface.DirectSocketInterface(hostname, port)
        self.merchant_id = merchant_id
        self.password = password
        self.customer = None
        self.order = None
        self.verification = None

    def write_header(self):
        if self.merchant_id == None or self.password == None:
            raise Exception("Merchant ID or password not specified.")
        self.socket.write("pg_merchant_id", self.merchant_id)
        self.socket.write("pg_password", self.password)
    
    def verify_with(self, verification):
        self.verification = verification
        return self

    def regarding_order(self, order):
        self.order = order
        return self

    def for_customer(self, customer):
        self.customer = customer
        return self

    def including_recurrence(self, recurrence):
        self.recurrence = recurrence
        return self

    def execute(self, operation={}, customer=None, order=None, verification=None, recurrence=None):
        self.write_header()
        if customer is not None:
            self.for_customer(customer)
        if order is not None:
            self.regarding_order(order)
        if verification is not None:
            self.verify_with(verification)
        if recurrence is not None:
            self.including_recurrence(recurrence)

        if self.customer:
            operation.update(self.customer.data)
        if self.order:
            operation.update(self.order)
        if self.verification:
            operation.update(self.verification.data)
        if self.recurrence:
            operation.update(self.recurrence.data)

        for key, value in operation.items():
            self.socket.write(key, value)
        self.socket.send()
        response = self.socket.read()
        if response['pg_response_type'] == 'E':
            raise Exception(response['pg_response_description'])
        if response['pg_response_type'] == 'D':
            raise DeclinedException(response['pg_trace_number'], response['pg_response_description'], response)
        return response['pg_trace_number'], response['pg_response_description'], response

    def close(self):
        return self.socket.close()

    def __del__(self):
        self.socket.close()
    
class DeclinedException(Exception):
    def __init__(self, id, message, response):
        self.message = message
        self.id = id
        self.response = response
    def __str__(self):
        return repr(self.message)

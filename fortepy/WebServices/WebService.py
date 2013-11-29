from suds.client import Client
import time, hmac

class WebService(object):
    API_LOGIN_ID = '5ot80D7XdD'
    TRANSACTION_KEY = '1NSa45VrQJk2j5'
    MERCHANT_ID = 160361
    CLIENT = Client('https://sandbox.paymentsgateway.net/WS/Client.wsdl')
    TRANSACTION = Client('https://sandbox.paymentsgateway.net/WS/Transaction.wsdl')

    def __init__(self, endpoint):
        self.__dict__['endpoint'] = endpoint
        self.__dict__['record'] = None
    
    @staticmethod
    def get_authentication(endpoint):
        auth = endpoint.factory.create('Authentication')
        auth.APILoginID = WebService.API_LOGIN_ID
        auth.UTCTime = "%d" % (time.time() * 10000000 + 621355968000000000)
        auth.TSHash = hmac.new(bytes(WebService.TRANSACTION_KEY, 'UTF-8'), bytes("%s|%s" % (WebService.API_LOGIN_ID, auth.UTCTime), 'UTF-8')).hexdigest()
        return auth

    @property
    def authentication(self):
        return WebService.get_authentication(self.endpoint)

    def __getattr__(self, name):
        if name == 'record':
            return self.__dict__['record']
        elif name not in self.__dict__['record'].__dict__:
            raise Exception("Property %s not found" % name)
        else:
            return self.__dict__['record'].__dict__[name]

    def __setattr__(self, name, value):
        if name == 'record':
            self.__dict__['record'] = value
        elif name not in self.__dict__['record'].__dict__:
            raise Exception("Property %s not found" % name)
        else:
            self.__dict__['record'].__dict__[name] = value

    def __str__(self):
        return str(self.record)
    def __repr__(self):
        return "<%s>" % str(self)
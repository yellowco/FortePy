from WebServices.WebService import WebService
from AGI.DirectSocketInterface import DirectSocketInterface

def config(merchant_id, api_login_id, transaction_key, agi_password):
    WebService.MERCHANT_ID = merchant_id
    WebService.API_LOGIN_ID = api_login_id
    WebService.TRANSACTION_KEY = transaction_key
    DirectSocketInterface.MERCHANT_ID = merchant_id
    DirectSocketInterface.AGI_PASSWORD = agi_password
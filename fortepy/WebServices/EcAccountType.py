from suds.client import Client
import WebService
EcAccountType = WebService.WebService.CLIENT.factory.create('EcAccountType')
CHECKING = EcAccountType['CHECKING']
SAVINGS = EcAccountType['SAVINGS']

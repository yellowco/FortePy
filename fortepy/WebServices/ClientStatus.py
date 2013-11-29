from suds.client import Client
import WebService
ClientStatus = WebService.WebService.CLIENT.factory.create('ClientStatus')
ACTIVE = ClientStatus['Active']
DELETED = ClientStatus['Deleted']
SUSPENDED = ClientStatus['Suspended']
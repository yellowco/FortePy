from suds.client import Client
import WebService
CcCardType = WebService.WebService.CLIENT.factory.create('CcCardType')
VISA = CcCardType['VISA']
MAST = CcCardType['MAST']
DISC = CcCardType['DISC']
AMER = CcCardType['AMER']
DINE = CcCardType['DINE']
JCB = CcCardType['JCB']
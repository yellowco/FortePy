class DriversLicense(object):
    def __init__(self, number, state):
        self.number = number
        self.state = state

    @property
    def data(self):
        return {'pg_billto_dl_number': self.number,
                'pg_billto_dl_state': self.state}


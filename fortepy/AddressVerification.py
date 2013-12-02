class AddressVerification(object):
    IGNORE = 0
    CHECK_ONLY = 1
    REQUIRE = 2

    def __init__(self, cc_zip=0, cc_street=0, state_zip=0, state_phone=0, email=0):
        self.cc_zip = cc_zip
        self.cc_street = cc_street
        self.state_zip = state_zip
        self.state_phone = state_phone
        self.email = email

    @property
    def code(self):
        return "%d%d%d%d%d" % (self.cc_zip, self.cc_street, self.state_zip, self.state_phone, self.email)
    

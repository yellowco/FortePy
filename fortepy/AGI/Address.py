class Address(object):
    def __init__(self, first_name, last_name, street1, street2, city, state, postal, country):
        self.first_name = first_name
        self.last_name = last_name
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.postal = postal
        self.country = country

    @property
    def data(self):
        return {'ecom_billto_postal_name_first': self.first_name,
                'ecom_billto_postal_name_last': self.last_name,
                'ecom_billto_postal_street_line1': self.street1,
                'ecom_billto_postal_street_line2': self.street2,
                'ecom_billto_postal_city': self.city,
                'ecom_billto_postal_stateprov': self.state,
                'ecom_billto_postal_postalcode': self.postal,
                'ecom_billto_postal_countrycode': self.country}
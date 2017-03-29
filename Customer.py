# Customer object with limited QBO fields to simplify this sample
class Customer:
    def __init__(self, f_name, l_name, m_name, phone, email):
        self.given_name = f_name
        self.middle_name = m_name
        self.family_name = l_name
        self.primary_phone = phone
        self.primary_email_addr = email

    def print_customer(self):
        print self.given_name, self.middle_name, self.family_name, self.primary_phone, self.primary_email_addr

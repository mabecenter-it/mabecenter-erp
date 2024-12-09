class ContactExist(Exception):
    def __init__(self, message, contact_name):
        super().__init__(message)
        self.contact_name = contact_name
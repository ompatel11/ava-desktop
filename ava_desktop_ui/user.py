class User:
    email = str
    uid = str
    prime_status = bool
    idtoken = str

    def __init__(self):
        self.email = ""
        self.uid = ""
        self.prime_status = False
        self.idtoken = ""

    def deleteData(self):
        self.email = None
        self.uid = None
        self.prime_status = None
        self.idtoken = None


current_user = User()

class User:
    email = str
    uid = str
    prime_status = bool
    idtoken = str
    task_list = list

    def __init__(self):
        self.email = ""
        self.uid = ""
        self.prime_status = False
        self.idtoken = ""
        self.task_list = []

    def addTask(self, data):
        self.task_list.append(data)

    def getTasks(self):
        import json
        f = open("application/config/tasks.json")
        data = json.load(f)
        for i in data['tasks']:
            print(i)
            self.task_list.append(i)
        f.close()
        print(self.task_list)

    def deleteData(self):
        self.email = None
        self.uid = None
        self.prime_status = None
        self.idtoken = None
        self.task_list = None


current_user = User()

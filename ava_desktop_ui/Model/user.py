import json
from ruamel import yaml


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
        with open('application/config/tasks.json', 'w') as data_file:
            print("Task List after adding:", self.task_list)
            json.dump(self.task_list, data_file)

    def deleteTask(self, taskname):
        with open('application/config/tasks.json') as data_file:
            data = json.load(data_file)
        print(data)
        index = 0
        for i in data:
            self.task_list.remove(i)
            if i['name'] == taskname:
                print(i)
                del data[index]
            index += 1

        with open('application/config/tasks.json', 'w') as data_file:
            print("Task List after deleting:", data)
            json.dump(data, data_file)

        yamlObj = yaml.YAML()
        with open('application/config/task_bindings.yml') as fp:
            data = yamlObj.load(fp)
            new_data = data
            del data

        with open('application/config/task_bindings.yml', 'w') as file:
            del new_data[taskname]
            yamlObj.dump(new_data, file)
        print(new_data)

    def getTasks(self):

        try:
            f = open("application/config/tasks.json")
            data = json.load(f)
            print(data)
            for i in data:
                print(i['name'])
                self.task_list.append(i)
            f.close()
        except Exception as e:
            print(e)
        print("Task list: ", self.task_list)

    def deleteData(self):
        self.email = None
        self.uid = None
        self.prime_status = None
        self.idtoken = None
        self.task_list = None

    def logout(self):
        data = json.load(open('application/config/tasks.json'))

        with open('application/config/tasks.json', 'w') as data_file:
            print("Task List after deleting:", data)
            json.dump('{}', data_file, indent=4)

        yamlObj = yaml.YAML()
        with open('application/config/task_bindings.yml', 'w') as file:
            yamlObj.dump('{}', file)


current_user = User()

import json
import os

from ruamel import yaml


class User:
    email = str
    uid = str
    prime_status = bool
    idtoken = str
    task_list = list
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    taskJsonFilePath = os.path.join(ROOT_DIR, '../application/config/tasks.json')
    taskBindingsFilePath = os.path.join(ROOT_DIR, '../application/config/task_bindings.yml')
    print(taskBindingsFilePath)
    print(taskJsonFilePath)

    def __init__(self):
        self.email = ""
        self.uid = ""
        self.prime_status = False
        self.idtoken = ""
        self.task_list = []

    def addTask(self, data):
        self.task_list.append(data)
        with open(self.taskJsonFilePath, 'w+') as data_file:
            print("Task List after adding:", self.task_list)
            json.dump(self.task_list, data_file)

    def deleteTask(self, taskname):
        with open(self.taskJsonFilePath) as data_file:
            data = json.load(data_file)
        print(data)
        index = 0
        for i in data:

            if i['name'] == taskname:
                print(i)
                del data[index]
                self.task_list.remove(i)
            index += 1
        if len(self.task_list) == 0:
            os.remove(self.taskJsonFilePath)
            os.remove(self.taskBindingsFilePath)
        else:
            with open(self.taskJsonFilePath, 'w+') as data_file:
                print("Task List after deleting:", data)
                json.dump(data, data_file)

            yamlObj = yaml.YAML()
            with open(self.taskBindingsFilePath, "w+") as fp:
                data = yamlObj.load(fp)
                new_data = data
                del data

            with open(self.taskBindingsFilePath, 'w+') as file:
                del new_data[taskname]
                yamlObj.dump(new_data, file)
            print(new_data)

    def getTasks(self):

        try:
            f = open(self.taskJsonFilePath)
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
        data = json.load(open(self.taskJsonFilePath))

        with open(self.taskJsonFilePath, 'w+') as data_file:
            print("Task List after deleting:", data)
            json.dump('{}', data_file, indent=4)

        yamlObj = yaml.YAML()
        with open(self.taskBindingsFilePath, 'w+') as file:
            yamlObj.dump('{}', file)


current_user = User()

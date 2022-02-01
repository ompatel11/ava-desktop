import json
import os

from ruamel import yaml

from .utils import get_project_root


class User:
    email = str
    name = str
    uid = str
    isVerified = str
    auth_token = str
    prime_status = bool
    idtoken = str
    task_list = list
    taskJsonFilePath = str(get_project_root()) + '/application/config/tasks.json'
    taskBindingsFilePath = str(get_project_root()) + '/application/config/task_bindings.yml'

    def __init__(self):
        self.email = ""
        self.name = ""
        self.uid = ""
        self.prime_status = False
        self.idtoken = ""
        self.task_list = []
        self.isVerified = "False"
        self.auth_token = ""

    def checkforappend(self, taskEntries):
        empty = bool
        with open("application/config/task_bindings.yml", 'w+') as fp:
            data = yaml.load_all(fp, Loader=yaml.Loader)
            print("DATA:", data)
            if data is None:
                print("Empty yaml file")
                empty = True
        if empty:
            print("Writing task to file")
            with open("application/config/task_bindings.yml", 'w+', encoding="utf-8") as yamlfile:
                yaml.dump_all(taskEntries, yamlfile,
                              Dumper=yaml.RoundTripDumper, default_flow_style=False)
            return False
        else:
            print("Appending task to file")
            with open('application/config/task_bindings.yml', 'a', encoding="utf-8") as yamlfile:
                yaml.dump(taskEntries, yamlfile,
                          Dumper=yaml.RoundTripDumper, default_flow_style=False)
            return True

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
                try:
                    if new_data[taskname]:
                        del new_data[taskname]
                        yamlObj.dump(new_data, file)
                except:
                    return None

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
        self.email = ''
        self.uid = ''
        self.prime_status = ''
        self.idtoken = ''
        self.task_list = []

    def logout(self):
        try:
            os.remove(self.taskJsonFilePath)
            os.remove(self.taskBindingsFilePath)
        except FileNotFoundError as e:
            print(e)


current_user = User()

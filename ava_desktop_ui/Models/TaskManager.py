class TaskManager:
    def __init__(self):
        self.taskList = []

    def addTask(self, task):
        self.taskList.append(task)

    def getTasks(self):
        return self.taskList


TaskLists = TaskManager()

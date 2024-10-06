import argparse
import datetime

class TaskManager:
    task_list = dict()
    
    def add_task(task):
        new_task_id = len(TaskManager.task_list) + 1
        new_task_description = task
        new_task_status = "todo"
        new_task_createdAt = datetime.datetime.now().strftime("%c")
        new_task_updatedAt = datetime.datetime.now().strftime("%c")
        new_task = dict(description=new_task_description,status=new_task_status,createdAt=new_task_createdAt,updatedAt=new_task_updatedAt)
        TaskManager.task_list[new_task_id] = new_task



parser = argparse.ArgumentParser(description='Task Tracker CLI App.')

parser.add_argument("action", type=str, help="Available commands: add")
parser.add_argument('args1')

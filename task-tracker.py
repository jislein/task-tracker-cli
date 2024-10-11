import argparse
import datetime
import json
import os

STATUS_TODO = "todo"
STATUS_DONE = 'done'
STATUS_IN_PROGRESS = "in-progress"

ERROR_TASK_LIST_EMPTY = "Error: Task list is emtpy."

JSON_FILE_PATH = "tasks_data.json"

STATUS_TODO = "todo"
STATUS_DONE = 'done'
STATUS_IN_PROGRESS = "in-progress"

ERROR_TASK_LIST_EMPTY = "Error: Task list is emtpy."

JSON_FILE_PATH = "tasks_data.json"

class TaskManager:
    # Where tasks are stored
    # Where tasks are stored
    task_list = dict()

    def add_task(self, task):
        new_task_id = len(self.task_list) + 1        
    def add_task(self, task):
        new_task_id = len(self.task_list) + 1        
        new_task_description = task
        new_task_status = STATUS_TODO
        new_task_status = STATUS_TODO
        new_task_createdAt = datetime.datetime.now().strftime("%c")
        new_task_updatedAt = datetime.datetime.now().strftime("%c")


        new_task = dict(description=new_task_description,status=new_task_status,createdAt=new_task_createdAt,updatedAt=new_task_updatedAt)
        self.task_list[new_task_id] = new_task
        print(f"New task added successfully (ID: {new_task_id}).")
        self.print_task(new_task_id)

        self.print_task(new_task_id)

        self.save_data()
    
    def update_task(self, task_id, new_description):
        if len(self.task_list) == 0:
            print(ERROR_TASK_LIST_EMPTY)
            print(ERROR_TASK_LIST_EMPTY)
            return

        if self.task_list.get(task_id) != None: 
            old_description = self.task_list[task_id]["description"]
            self.task_list[task_id]["description"] = new_description
            # self.description_col_spacing = len(str(new_description)) if len(str(self.description_col_spacing)) < len(str(new_description)) else self.description_col_spacing
            # self.description_col_spacing = len(str(new_description)) if len(str(self.description_col_spacing)) < len(str(new_description)) else self.description_col_spacing
            self.task_updated(task_id)
            print(f"Task updated successfully\nFrom: {old_description}\n To: {self.task_list[task_id]["description"]}")        
            self.save_data()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")

    def delete_task(self, task_id):
        if len(self.task_list) == 0:
            print(ERROR_TASK_LIST_EMPTY)
            print(ERROR_TASK_LIST_EMPTY)
            return
        
        
        if self.task_list.get(task_id) != None:
            if len(self.task_list) == 1:
                self.task_list.pop(task_id)
                print("Task deleted successfully.")
                self.save_data()
            elif task_id == str(len(self.task_list)):
                self.task_list.pop(task_id)
                print("Task deleted LAST successfully.")
                self.save_data()
            elif task_id == str(len(self.task_list)):
                self.task_list.pop(task_id)
                print("Task deleted LAST successfully.")
                self.save_data()
            else:
                self.task_list.pop(task_id)
                new_dict = dict()
                # When there are more than 1 task and the task deleted is not the last one, we need to re-assign the IDs
                # When there are more than 1 task and the task deleted is not the last one, we need to re-assign the IDs
                for count, key in enumerate(self.task_list, start=1):
                    new_dict[count] = self.task_list.get(key)                
                #print(new_dict)
                self.task_list = new_dict.copy()
                # print(self.task_list)
                print("Task deleted successfully.")
                print("Task deleted successfully.")
                self.save_data()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")
    
    def update_status(self, task_id, new_status):
        if len(self.task_list) == 0:
            print(ERROR_TASK_LIST_EMPTY)
            print(ERROR_TASK_LIST_EMPTY)
            return
        if self.task_list.get(task_id) != None:
            if new_status == self.task_list[task_id]["status"]:
                print(f"Task already {new_status}.")
            if new_status == self.task_list[task_id]["status"]:
                print(f"Task already {new_status}.")
            self.task_list[task_id]["status"] = new_status
            self.task_updated(task_id)
            self.save_data()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")

    # If no argument is passed then lists all tasks.
    # If no argument is passed then lists all tasks.
    def list_tasks(self, args):
        if len(self.task_list) == 0:
            print(ERROR_TASK_LIST_EMPTY)
            print(ERROR_TASK_LIST_EMPTY)
            return
        if args.done:
            self.print_list(STATUS_DONE)            
            self.print_list(STATUS_DONE)            
            return
        elif args.todo:
            self.print_list(STATUS_TODO)            
            self.print_list(STATUS_TODO)            
            return
        elif args.in_progress:
            self.print_list(STATUS_IN_PROGRESS)
            self.print_list(STATUS_IN_PROGRESS)
            return
        else:
            self.print_list()            

    def print_list(self, status="all"):        
        if status == STATUS_DONE:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        elif status == STATUS_TODO:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        elif status == STATUS_IN_PROGRESS:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        else:
            self.print_list()            

    def print_list(self, status="all"):        
        if status == STATUS_DONE:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        elif status == STATUS_TODO:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        elif status == STATUS_IN_PROGRESS:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)
        else:
            for task_id in self.task_list:
                self.print_task(task_id)
    
    # Updates the date of the updatedAt attribute
                self.print_task(task_id)
    
    # Updates the date of the updatedAt attribute
    def task_updated(self, task_id):
            task_updatedAt = datetime.datetime.now().strftime("%c")
            self.task_list[task_id]["updatedAt"] = task_updatedAt
            
            
    # Saves tasks to a JSON file.
    def save_data(self):
        print("Saving to JSON file...")
        with open(JSON_FILE_PATH, "w") as outfile:
        with open(JSON_FILE_PATH, "w") as outfile:
            json.dump(self.task_list,outfile,indent=4)
            print("JSON file updated successfully.")
    
    # Load tasks from a JSON file.
    def load_data(self):
        
        with open(JSON_FILE_PATH, "r") as json_file:
        
        with open(JSON_FILE_PATH, "r") as json_file:
            self.task_list = json.loads(json_file.read())
            print("JSON file loaded successfully.")
    
    def print_task(self, task_id):
        task = self.task_list[task_id]
        
        spacing = "| {:<9} | {:<" + f"{11 if len(task["description"])+2<11 else len(task["description"])+2}"+"} | {:<" + f"{8 if len(task["status"])<11 else len(task["status"])+2}"+"} | {:<" + f"{24+2}"+"} | {:<" + f"{len(task["updatedAt"])}"+"} |"
        
        header = spacing.format("Task ID", "Description", "Status", "Creation date", "Last updated")
        elements = spacing.format(str(task_id), task["description"], task["status"], task["createdAt"], task["updatedAt"])

        border = ""
        corner = "+"

        for i in range(len(elements)-2):
            border += "-"

        print(corner + border + corner)
        print(header)
        print(corner + border + corner)
        print(elements)
        print(corner + border + corner)
            print("JSON file loaded successfully.")
    
    def print_task(self, task_id):
        task = self.task_list[task_id]
        
        spacing = "| {:<9} | {:<" + f"{11 if len(task["description"])+2<11 else len(task["description"])+2}"+"} | {:<" + f"{8 if len(task["status"])<11 else len(task["status"])+2}"+"} | {:<" + f"{24+2}"+"} | {:<" + f"{len(task["updatedAt"])}"+"} |"
        
        header = spacing.format("Task ID", "Description", "Status", "Creation date", "Last updated")
        elements = spacing.format(str(task_id), task["description"], task["status"], task["createdAt"], task["updatedAt"])

        border = ""
        corner = "+"

        for i in range(len(elements)-2):
            border += "-"

        print(corner + border + corner)
        print(header)
        print(corner + border + corner)
        print(elements)
        print(corner + border + corner)

def main():

    # Creates TaskManager object to handle tasks operations
    tm = TaskManager()
    # Checks if there is any data to load.
    if os.path.isfile(JSON_FILE_PATH):
        tm.load_data()
    else:
        print("JSON file not found. A new file will be created.")
        with open(JSON_FILE_PATH, "w") as json_file:
            json_file.write("{}")
            print(f"File '{JSON_FILE_PATH}' successfully created.\n")
    if os.path.isfile(JSON_FILE_PATH):
        tm.load_data()
    else:
        print("JSON file not found. A new file will be created.")
        with open(JSON_FILE_PATH, "w") as json_file:
            json_file.write("{}")
            print(f"File '{JSON_FILE_PATH} successfully created.\n")
        tm.load_data()

    parser = argparse.ArgumentParser(description='Task Tracker CLI App.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands to run: add, update, delete, list, mark-in-progress, mark-done, mark-todo', required=True)
    subparsers = parser.add_subparsers(dest='command', help='Available commands to run: add, update, delete, list, mark-in-progress, mark-done, mark-todo', required=True)

    add_task = subparsers.add_parser('add', help='Add a task to the task list. Default status: todo')
    add_task.add_argument("task_description", type=str, help="Task description must be inside quotes or double quotes.")

    update_task = subparsers.add_parser('update', help='Updates task description.')
    update_task.add_argument('id', type=str, help="id number of the task that will be updated.")
    update_task.add_argument('new_description', type=str, help="New description must be inside quotes or double quotes.")

    delete_task = subparsers.add_parser('delete', help='Delete task.')
    delete_task.add_argument('id', type=str, help="id number of the task that will be deleted.")

    task_in_progress = subparsers.add_parser('mark-in-progress', help='Mark task as in progress.')
    task_in_progress = subparsers.add_parser('mark-in-progress', help='Mark task as in progress.')
    task_in_progress.add_argument('id', type=str, help="id number of the task.")

    task_done = subparsers.add_parser('mark-done', help='Mark task as done.')
    task_done = subparsers.add_parser('mark-done', help='Mark task as done.')
    task_done.add_argument('id', type=str, help="id number of the task.")

    task_todo = subparsers.add_parser('mark-todo', help='Mark task as to do.')
    task_todo.add_argument('id', type=str, help="id number of the task.")

    task_todo = subparsers.add_parser('mark-todo', help='Mark task as to do.')
    task_todo.add_argument('id', type=str, help="id number of the task.")

    list_tasks = subparsers.add_parser('list', usage="list [option]" ,description='Shows tasks.')
    list_tasks.add_argument("--in-progress", "-i", action="store_true", help="Shows all tasks with status: in-progress")
    list_tasks.add_argument("--done", '-d', action="store_true", help="Shows all tasks with status: done")
    list_tasks.add_argument("--todo", "-t", action="store_true", help="Shows all tasks with status: todo")
    
    
    args = parser.parse_args()

    if args.command == 'add':
        tm.add_task(args.task_description)
    elif args.command == 'update':
        tm.update_task(args.id,args.new_description)
    elif args.command == 'delete':
        tm.delete_task(args.id)
    elif args.command == 'mark-in-progress':
        tm.update_status(args.id, STATUS_IN_PROGRESS)
        tm.update_status(args.id, STATUS_IN_PROGRESS)
    elif args.command == 'mark-done':
        tm.update_status(args.id, STATUS_DONE)
    elif args.command == 'mark-todo':
        tm.update_status(args.id, STATUS_TODO)
        tm.update_status(args.id, STATUS_DONE)
    elif args.command == 'mark-todo':
        tm.update_status(args.id, STATUS_TODO)
    elif args.command == 'list':
        tm.list_tasks(args)

if __name__ == '__main__':
    main()
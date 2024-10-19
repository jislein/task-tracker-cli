import argparse
import datetime
import json
import os


STATUS_TODO = "todo"
STATUS_DONE = 'done'
STATUS_IN_PROGRESS = "in-progress"

ERROR_TASK_LIST_EMPTY = "Error: Task list is emtpy."

JSON_FILE_PATH = "tasks_data.json"

USAGE_MESSAGE = f'%(prog)s [option]\n{"or:":>6} %(prog)s command [option]\n{"":>8}command: the positional argument\n'

class TaskManager:

    # TODO:
    # A JSON file that saves the task list and the task coutners

    # Where tasks are stored
    task_list = dict()

    # Keeps track of how many of each status there are.
    # Used this method to avoid looping through the task_list when trying 
    # to list tasks with a status that does not exist.
    tasks_done = 0
    tasks_todo = 0
    tasks_in_progress = 0

    def add_task(self, task):
        new_task_id = len(self.task_list) + 1        
        new_task_description = task
        new_task_status = STATUS_TODO
        new_task_createdAt = datetime.datetime.now().strftime("%c")
        new_task_updatedAt = datetime.datetime.now().strftime("%c")

        new_task = dict(description=new_task_description,status=new_task_status,createdAt=new_task_createdAt,updatedAt=new_task_updatedAt)
        self.task_list[new_task_id] = new_task
        self.increase_status_amount()
        print_success(f"New task added successfully (ID: {new_task_id}).")
        self.print_task(new_task_id)

        self.save_data()
    
    # Changes task description.
    def update_task(self, task_id, new_description):
        if len(self.task_list) == 0:
            print_error(ERROR_TASK_LIST_EMPTY)
            return

        if self.task_list.get(task_id) != None: 
            old_description = self.task_list[task_id]["description"]
            self.task_list[task_id]["description"] = new_description
            # self.description_col_spacing = len(str(new_description)) if len(str(self.description_col_spacing)) < len(str(new_description)) else self.description_col_spacing
            self.task_updated(task_id)
            print_success(f"Task updated successfully\nFrom: {old_description}\n To: {self.task_list[task_id]["description"]}")        
            self.save_data()
        else:
            print_error(f"Error: Task with ID: {task_id} does not exist.")

    def delete_task(self, task_id):
        # Here we check if the list is empty.
        if len(self.task_list) == 0:
            print_error(ERROR_TASK_LIST_EMPTY)
            return
        # Checks if the tasks exist.
        if self.task_list.get(task_id) != None:
            # Do a simple pop() if there is only one task in the list
            if len(self.task_list) == 1:
                deleted_task = self.task_list.pop(task_id)
                print_success("Task deleted successfully.")
                self.decrease_status_amount(deleted_task[task_id]["status"])
                self.save_data()
            elif task_id == str(len(self.task_list)):
                deleted_task = self.task_list.pop(task_id)
                print_success("Task deleted successfully.")
                self.decrease_status_amount(deleted_task[task_id]["status"])
                self.save_data()
            else:
                deleted_task = self.task_list.pop(task_id)
                new_dict = dict()
                # When there are more than 1 task and the task deleted is not the last one, we need to re-assign the IDs
                for count, key in enumerate(self.task_list, start=1):
                    new_dict[count] = self.task_list.get(key)
                self.task_list = new_dict.copy()
                print_success("Task deleted successfully.")
                self.decrease_status_amount(deleted_task["status"])
                self.save_data()
        else:
            print_error(f"Error: Task with ID: {task_id} does not exist.")
    
    def update_status(self, task_id, new_status):
        
        if len(self.task_list) == 0:
            print_error(ERROR_TASK_LIST_EMPTY)
            return
        # First we check if the task exist.
        if self.task_list.get(task_id) != None:
            current_status = self.task_list[task_id]["status"]
            # Here we check if the current status is the same as the new status.
            if new_status == current_status:
                print_error(f"Error: Task already with status: {new_status}.")
                return
            self.increase_status_amount(new_status)
            self.decrease_status_amount(current_status)
            self.task_list[task_id]["status"] = new_status

            self.task_updated(task_id)
            self.save_data()
        else:
            print_error(f"Error: Task with ID: {task_id} does not exist.")

    # If no argument is passed then lists all tasks.
    def list_tasks(self, args):
        if len(self.task_list) == 0:
            print_error(ERROR_TASK_LIST_EMPTY)
            return        
        if args.done:
            self.print_list(STATUS_DONE)            
            return
        elif args.todo:
            self.print_list(STATUS_TODO)            
            return
        elif args.in_progress:
            self.print_list(STATUS_IN_PROGRESS)
            return
        else:
            self.print_list()            

    def print_list(self, status="all"):        
        if status != "all":
            if status == STATUS_DONE and self.tasks_done == 0:
                print_error(f"Error: There are no tasks marked as: {STATUS_DONE}")
                return
            if status == STATUS_TODO and self.tasks_todo == 0:
                print_error(f"Error: There are no tasks marked as: {STATUS_TODO}")
                return
            if status == STATUS_IN_PROGRESS and self.tasks_in_progress == 0:
                print_error(f"Error: There are no tasks marked as: {STATUS_IN_PROGRESS}")
                return
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == status:                    
                    self.print_task(task_id)        
        else:
            for task_id in self.task_list:
                self.print_task(task_id)
    
    # Prints a table with task information
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

    def print_status_count(self):
        print(f"Total tasks todo: {self.tasks_todo}\nTotal tasks done: {self.tasks_done}\nTotal tasks in-progress: {self.tasks_in_progress}")

    # Updates the date of the updatedAt attribute
    def task_updated(self, task_id):
            task_updatedAt = datetime.datetime.now().strftime("%c")
            self.task_list[task_id]["updatedAt"] = task_updatedAt
    
    def decrease_status_amount(self, status="todo"):
        if status != "todo":
            if status == STATUS_DONE:
                self.tasks_done = max(0, self.tasks_done - 1)
            else:
                self.tasks_in_progress = max(0, self.tasks_in_progress- 1)
        else:
            self.tasks_todo = max(0, self.tasks_todo- 1)
    
    def increase_status_amount(self, status="todo"):
        if status != "todo":
            if status == STATUS_DONE:
                self.tasks_done += 1
            else:
                self.tasks_in_progress += 1
        else:
            self.tasks_todo += 1

    # TODO: store the values on a dictionary and add it to a JSON file algonside the task list.
    def update_status_count(self):
        # self.print_status_count()
        total_tasks = self.tasks_done + self.tasks_todo + self.tasks_in_progress

        for key in self.task_list:
            if self.task_list[key]["status"] == STATUS_DONE:
                self.increase_status_amount(STATUS_DONE)
            elif self.task_list[key]["status"] == STATUS_IN_PROGRESS:
                self.increase_status_amount(STATUS_IN_PROGRESS)
            elif self.task_list[key]["status"] == STATUS_TODO:
                self.increase_status_amount()
        total_tasks = self.tasks_done + self.tasks_todo + self.tasks_in_progress
        
        if total_tasks == len(self.task_list):
            print_success("Status counters loaded successfully.")
        else:
            print_error("Error: Status counters failed to load.")

    # Saves tasks to a JSON file.
    def save_data(self):
        print("Saving to JSON file...")
        with open(JSON_FILE_PATH, "w") as outfile:
            json.dump(self.task_list,outfile,indent=4)
            print_success("JSON file updated successfully.")
    
    # Load tasks from a JSON file.
    def load_data(self):        
        with open(JSON_FILE_PATH, "r") as json_file:
            self.task_list = json.loads(json_file.read())
            print_success("JSON file loaded successfully.")
        if self.tasks_done + self.tasks_todo + self.tasks_in_progress != len(self.task_list):
            self.update_status_count()
        else:
            return
    
# Uses ANSI Escape Codes to color the messages. For more info check this site: https://ozzmaker.com/add-colour-to-text-in-python/
def print_error(message):
    print("\033[1;31;40m " + message + "\033[0;0m")

def print_warning(message):
    print("\033[1;33;40m " + message + "\033[0;0m")

def print_success(message):
    print("\033[1;32;40m " + message + "\033[0;0m")


def main():
    # TODO: Check if there are other areas to improve in the usage messages.
    parser = argparse.ArgumentParser(usage=USAGE_MESSAGE, description='Task Tracker CLI App.\nUse -h or --help next to a command to get more info on how to use it.')
    subparsers = parser.add_subparsers(dest='command', required=True, metavar="")

    add_task = subparsers.add_parser('add', help='Add a task to the task list. Default status: todo.', prog="add", usage=f"{parser.prog} add task_description")
    add_task.add_argument("task_description", type=str, help="Task description must be inside quotes or double quotes if it contains white space/s.")

    update_task = subparsers.add_parser('update', help='Updates task description.', prog="update", usage=f"{parser.prog} update id new_description")
    update_task.add_argument('id', type=str, help="id number of the task that will be updated.")
    update_task.add_argument('new_description', type=str, help="New description must be inside quotes or double quotes if it contains white space/s.")

    delete_task = subparsers.add_parser('delete', help='Delete task.', prog="delete", usage=f"{parser.prog} delete id")
    delete_task.add_argument('id', type=str, help="id number of the task that will be deleted.")

    list_tasks = subparsers.add_parser('list', help="Lists tasks.", prog="list", usage=f"{parser.prog} list [option]", description='Shows all tasks if no option is passed.')
    list_tasks.add_argument("-i", "--in-progress", action="store_true", help="Shows all tasks with status: in-progress")
    list_tasks.add_argument('-d', "--done", action="store_true", help="Shows all tasks with status: done")
    list_tasks.add_argument("-t", "--todo", action="store_true", help="Shows all tasks with status: todo")
    
    task_todo = subparsers.add_parser('mark-todo', help='Mark task as to do.', prog="mark-todo", usage=f"{parser.prog} mark-todo id")
    task_todo.add_argument('id', type=str, help="id number of the task.")
    
    task_done = subparsers.add_parser('mark-done', help='Mark task as done.', prog="mark-done", usage=f"{parser.prog} mark-done id")
    task_done.add_argument('id', type=str, help="id number of the task.")

    task_in_progress = subparsers.add_parser('mark-in-progress', help='Mark task as in progress.', prog="mark-in-progress", usage=f"{parser.prog} mark-in-progress id")
    task_in_progress.add_argument('id', type=str, help="id number of the task.")

    args = parser.parse_args()

    # Creates TaskManager object to handle tasks operations
    tm = TaskManager()
    # Checks if there is any data to load.
    if os.path.isfile(JSON_FILE_PATH):
        tm.load_data()
    else:
        print_warning("JSON file not found. A new file will be created.")
        with open(JSON_FILE_PATH, "w") as json_file:
            json_file.write("{}")
            print_success(f"File '{JSON_FILE_PATH} successfully created.\n")
        tm.load_data()

    if args.command == 'add':
        tm.add_task(args.task_description)
    elif args.command == 'update':
        tm.update_task(args.id,args.new_description)
    elif args.command == 'delete':
        tm.delete_task(args.id)
    elif args.command == 'mark-in-progress':
        tm.update_status(args.id, STATUS_IN_PROGRESS)
    elif args.command == 'mark-done':
        tm.update_status(args.id, STATUS_DONE)
    elif args.command == 'mark-todo':
        tm.update_status(args.id, STATUS_TODO)
    elif args.command == 'list':
        tm.list_tasks(args)

if __name__ == '__main__':
    main()
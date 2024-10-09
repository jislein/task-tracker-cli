import argparse
import datetime
import json
import os

class TaskManager:
    task_list = dict()
    DEFAULT_STATUS = "todo"

    def add_task(self, task) -> None:
        new_task_id = len(self.task_list) + 1
        new_task_description = task
        new_task_status = self.DEFAULT_STATUS
        new_task_createdAt = datetime.datetime.now().strftime("%c")
        new_task_updatedAt = datetime.datetime.now().strftime("%c")
        new_task = dict(description=new_task_description,status=new_task_status,createdAt=new_task_createdAt,updatedAt=new_task_updatedAt)
        self.task_list[new_task_id] = new_task
        print(f"New task added successfully (ID: {new_task_id}).")
        self.save_to_file()
        #print(self.task_list)
    
    def update_task(self, task_id, new_description):
        # print(self.task_list[str(task_id)])
        if len(self.task_list) == 0:
            print("Error: Task list is emtpy.")
            return

        if self.task_list.get(task_id) != None: 
            old_description = self.task_list[task_id]["description"]
            self.task_list[task_id]["description"] = new_description
            self.task_updated(task_id)
            print(f"Task updated successfully\nFrom: {old_description}\n To: {self.task_list[task_id]["description"]}")        
            self.save_to_file()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")

    def delete_task(self, task_id):
        if len(self.task_list) == 0:
            print("Error: Task list is emtpy.")
            return
        if self.task_list.get(task_id) != None:
            if len(self.task_list) == 1:
                self.task_list.pop(task_id)
                print("Task deleted successfully.")
                self.save_to_file()
            else:
                self.task_list.pop(task_id)
                new_dict = dict()
                for count, key in enumerate(self.task_list, start=1):
                    new_dict[count] = self.task_list.get(key)                
                #print(new_dict)
                self.task_list = new_dict.copy()
                # print(self.task_list)
                self.save_to_file()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")
    
    def update_status(self, task_id, new_status):
        if len(self.task_list) == 0:
            print("Error: Task list is emtpy.")
            return
        if self.task_list.get(task_id) != None:
            self.task_list[task_id]["status"] = new_status
            self.task_updated(task_id)
            self.save_to_file()
        else:
            print(f"Error: Task with ID: {task_id} does not exist.")

    def list_tasks(self, args):
        if args.done:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == "done":
                    print(f"Task ID{ ":":>6} {task_id}")
                    for key, value in self.task_list.get(task_id).items():                
                        print(f"{key:<12}: {value}")
                print()
            return
        elif args.todo:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == "todo":
                    print(f"Task ID{ ":":>6} {task_id}")
                    for key, value in self.task_list.get(task_id).items():                
                        print(f"{key:<12}: {value}")
                print()
            return
        elif args.in_progress:
            for task_id in self.task_list:
                if self.task_list[task_id]["status"] == "in-progress":
                    print(f"Task ID{ ":":>6} {task_id}")
                    for key, value in self.task_list.get(task_id).items():                
                        print(f"{key:<12}: {value}")
                print()
            return
        else:
            for task_id in self.task_list:
                print(f"Task ID{ ":":>6} {task_id}")
                for key, value in self.task_list.get(task_id).items():                
                    print(f"{key:<12}: {value}")
                print()

    def task_updated(self, task_id):
            task_updatedAt = datetime.datetime.now().strftime("%c")
            self.task_list[task_id]["updatedAt"] = task_updatedAt




    def save_to_file(self):
        print("Saving to JSON file...")
        with open("tasks.json", "w") as outfile:
            json.dump(self.task_list,outfile,indent=4)
            print("JSON file updated successfully.")
    
    def load_json(self):
        with open("tasks.json", "r") as json_file:
            self.task_list = json.loads(json_file.read())
            #print("JSON file loaded successfully.")
            
    
        


def main():
    tm = TaskManager()
    if os.path.isfile("tasks.json"):
        tm.load_json()

    parser = argparse.ArgumentParser(description='Task Tracker CLI App.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands to run: add, update, delete', required=True)

    add_task = subparsers.add_parser('add', help='Add a task to the task list. Default status: todo')
    add_task.add_argument("task_description", type=str, help="Task description must be inside quotes or double quotes.")

    update_task = subparsers.add_parser('update', help='Updates task description.')
    update_task.add_argument('id', type=str, help="id number of the task that will be updated.")
    update_task.add_argument('new_description', type=str, help="New description must be inside quotes or double quotes.")

    delete_task = subparsers.add_parser('delete', help='Delete task.')
    delete_task.add_argument('id', type=str, help="id number of the task that will be deleted.")

    task_in_progress = subparsers.add_parser('mark-in-progress', help='Mark task as "in-progress".')
    task_in_progress.add_argument('id', type=str, help="id number of the task.")

    task_done = subparsers.add_parser('mark-done', help='Mark task as "done".')
    task_done.add_argument('id', type=str, help="id number of the task.")

    list_tasks = subparsers.add_parser('list', usage="list [option]" ,description='Shows tasks.')
    list_tasks.add_argument("--in-progress", "-i", action="store_true", help="Shows all tasks with status: in-progress")
    list_tasks.add_argument("--done", '-d', action="store_true", help="Shows all tasks with status: done")
    list_tasks.add_argument("--todo", "-t", action="store_true", help="Shows all tasks with status: todo")
    

    args = parser.parse_args()


    if args.command == 'add':
        # print(args.task_description)
        # print(tm.DEFAULT_STATUS)
        # print(new_task)
        tm.add_task(args.task_description)
    elif args.command == 'update':
        tm.update_task(args.id,args.new_description)
    elif args.command == 'delete':
        tm.delete_task(args.id)
    elif args.command == 'mark-in-progress':
        tm.update_status(args.id, "in-progress")
    elif args.command == 'mark-done':
        tm.update_status(args.id, "done")
    elif args.command == 'list':
        tm.list_tasks(args)
        
    

if __name__ == '__main__':
    main()
# Task Tracker

This is my solution for the [task-tracker](https://roadmap.sh/projects/task-tracker) challenge from [roadmap.sh](https://roadmap.sh/).

## Features

- Add a new task with a description and save it to a JSON file.
- Update the description of an existing task.
- Delete a task.
- List all tasks or filter them by status: `todo`, `in-progress` or `done`.
- Mark tasks as: `in-progress`, `done` or `todo`.

## Requirements

You must have installed Python 3.7 or greater to use this program.

[Click here to download Python.](https://www.python.org/downloads/)

## Installation

Clone the repository and `cd` to the project folder:

```bash
git clone https://github.com/jislein/task-tracker-cli.git
cd task-tracker-cli
```

## Usage

You can use `-h` or `--help` with any command to see its usage message.

```bash
task-tracker.py --help # To see the list of available commands
```

**Add a task**:
```bash
task-tracker.py add "Buy groceries"
```

**Update a task**:
```bash
task-tracker.py update 1 "Buy groceries and cook dinner"
```

**Delete a task**:
```bash
task-tracker.py delete 1
```

**Mark a task as: `in-progress`, `done` or `todo`**:
```bash
task-tracker.py mark-in-progress 1
task-tracker.py mark-done 1
task-tracker.py mark-todo 1
```

**List all tasks**:
```bash
task-tracker.py list
```

**List task by its status**:
```bash
task-tracker.py list --done
task-tracker.py list --todo
task-tracker.py list --in-progress
```


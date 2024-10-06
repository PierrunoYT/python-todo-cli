# Todo List Manager

A feature-rich command-line todo list application written in Python.

## Features

- Add, list, complete, delete, and edit tasks
- Set due dates, priorities, and categories for tasks
- Add and manage subtasks
- Colorized output for better readability
- Search tasks by keyword
- Archive completed tasks
- Undo functionality
- Recurring tasks (daily, weekly, monthly)

## Requirements

- Python 3.6+
- colorama library

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/PierrunoYT/python-todo-cli.git
   cd python-todo-cli
   ```

2. Install the required library:
   ```
   pip install colorama
   ```

## Usage

Run the application:

```
python todo_manager.py
```

Follow the on-screen prompts to manage your tasks. Available commands:

- `add`: Add a new task
- `list`: List all tasks (with optional sorting)
- `complete`: Mark a task as completed
- `delete`: Delete a task
- `edit`: Edit an existing task
- `details`: Show details of a specific task
- `search`: Search tasks by keyword
- `archive`: Archive completed tasks
- `undo`: Undo the last action
- `add_subtask`: Add a subtask to an existing task
- `complete_subtask`: Mark a subtask as completed
- `quit`: Save and exit the application

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script. Archived tasks are saved in `archived_tasks.json`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

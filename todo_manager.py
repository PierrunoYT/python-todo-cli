import json
import os
from datetime import datetime, date, timedelta
from enum import Enum
import re
from colorama import init, Fore, Style

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class RecurrenceType(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3

# Initialize colorama
init(autoreset=True)

def colorize(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None

def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            return json.load(f)
    return []

undo_stack = []

def save_tasks(tasks, filename='tasks.json'):
    with open(filename, 'w') as f:
        json.dump(tasks, f)

def add_task(tasks, description, due_date=None, priority=None, category=None, recurrence=None):
    undo_stack.append(tasks.copy())
    task = {
        "description": description,
        "completed": False,
        "created_at": date.today().isoformat(),
        "due_date": due_date.isoformat() if due_date else None,
        "priority": priority.name if priority else None,
        "category": category,
        "recurrence": recurrence.name if recurrence else None,
        "subtasks": []
    }
    tasks.append(task)
    print(colorize("Task added successfully.", Fore.GREEN))

def list_tasks(tasks, sort_by=None):
    if not tasks:
        print(colorize("No tasks found.", Fore.YELLOW))
        return

    if sort_by == "due_date":
        sorted_tasks = sorted(tasks, key=lambda x: x["due_date"] or "9999-12-31")
    elif sort_by == "priority":
        priority_order = {None: 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}
        sorted_tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]], reverse=True)
    else:
        sorted_tasks = tasks

    for i, task in enumerate(sorted_tasks, 1):
        status = colorize("✓", Fore.GREEN) if task["completed"] else colorize("✗", Fore.RED)
        due_date = colorize(f" (Due: {task['due_date']})", Fore.CYAN) if task['due_date'] else ""
        priority_color = Fore.RED if task['priority'] == 'HIGH' else Fore.YELLOW if task['priority'] == 'MEDIUM' else Fore.GREEN
        priority = colorize(f" [Priority: {task['priority']}]", priority_color) if task['priority'] else ""
        category = colorize(f" #{task['category']}", Fore.MAGENTA) if task['category'] else ""
        print(f"{i}. [{status}] {task['description']}{due_date}{priority}{category}")
        
        if task['subtasks']:
            for j, subtask in enumerate(task['subtasks'], 1):
                subtask_status = colorize("✓", Fore.GREEN) if subtask["completed"] else colorize("✗", Fore.RED)
                print(f"   {i}.{j} [{subtask_status}] {subtask['description']}")

def complete_task(tasks, index):
    undo_stack.append(tasks.copy())
    if 1 <= index <= len(tasks):
        tasks[index-1]["completed"] = True
        print("Task marked as completed.")
    else:
        print("Invalid task number.")

def delete_task(tasks, index):
    undo_stack.append(tasks.copy())
    if 1 <= index <= len(tasks):
        del tasks[index-1]
        print("Task deleted successfully.")
    else:
        print("Invalid task number.")

def edit_task(tasks, index):
    undo_stack.append(tasks.copy())
    if 1 <= index <= len(tasks):
        task = tasks[index-1]
        print(f"Editing task: {task['description']}")
        
        new_description = input("Enter new description (or press Enter to keep current): ")
        if new_description:
            task['description'] = new_description

        new_due_date = input("Enter new due date (YYYY-MM-DD) (or press Enter to keep current): ")
        if new_due_date:
            parsed_date = parse_date(new_due_date)
            if parsed_date:
                task['due_date'] = parsed_date.isoformat()

        new_priority = input("Enter new priority (LOW/MEDIUM/HIGH) (or press Enter to keep current): ").upper()
        if new_priority in ('LOW', 'MEDIUM', 'HIGH'):
            task['priority'] = new_priority

        new_category = input("Enter new category (or press Enter to keep current): ")
        if new_category:
            task['category'] = new_category

        new_recurrence = input("Enter new recurrence (DAILY/WEEKLY/MONTHLY) (or press Enter to keep current): ").upper()
        if new_recurrence in ('DAILY', 'WEEKLY', 'MONTHLY'):
            task['recurrence'] = new_recurrence

        print("Task updated successfully.")
    else:
        print("Invalid task number.")

def show_task_details(tasks, index):
    if 1 <= index <= len(tasks):
        task = tasks[index-1]
        print(f"Task details for task {index}:")
        print(f"Description: {task['description']}")
        print(f"Status: {'Completed' if task['completed'] else 'Not completed'}")
        print(f"Created at: {task['created_at']}")
        print(f"Due date: {task['due_date'] or 'Not set'}")
        print(f"Priority: {task['priority'] or 'Not set'}")
        print(f"Category: {task['category'] or 'Not set'}")
        print(f"Recurrence: {task['recurrence'] or 'Not set'}")
    else:
        print("Invalid task number.")

def handle_recurring_tasks(tasks):
    today = date.today()
    for task in tasks:
        if task['recurrence'] and task['due_date']:
            due_date = datetime.strptime(task['due_date'], "%Y-%m-%d").date()
            if due_date <= today:
                if task['recurrence'] == 'DAILY':
                    new_due_date = today + timedelta(days=1)
                elif task['recurrence'] == 'WEEKLY':
                    new_due_date = today + timedelta(weeks=1)
                elif task['recurrence'] == 'MONTHLY':
                    new_due_date = today + timedelta(days=30)  # Approximation
                
                task['due_date'] = new_due_date.isoformat()
                task['completed'] = False

def search_tasks(tasks, keyword):
    matching_tasks = []
    for i, task in enumerate(tasks, 1):
        if keyword.lower() in task['description'].lower():
            matching_tasks.append((i, task))
    return matching_tasks

def add_subtask(tasks, parent_index, description):
    undo_stack.append(tasks.copy())
    if 1 <= parent_index <= len(tasks):
        subtask = {
            "description": description,
            "completed": False
        }
        tasks[parent_index-1]["subtasks"].append(subtask)
        print(colorize("Subtask added successfully.", Fore.GREEN))
    else:
        print(colorize("Invalid task number.", Fore.RED))

def complete_subtask(tasks, parent_index, subtask_index):
    undo_stack.append(tasks.copy())
    if 1 <= parent_index <= len(tasks):
        subtasks = tasks[parent_index-1]["subtasks"]
        if 1 <= subtask_index <= len(subtasks):
            subtasks[subtask_index-1]["completed"] = True
            print(colorize("Subtask marked as completed.", Fore.GREEN))
        else:
            print(colorize("Invalid subtask number.", Fore.RED))
    else:
        print(colorize("Invalid task number.", Fore.RED))

def main():
    tasks = load_tasks()
    
    while True:
        handle_recurring_tasks(tasks)
        command = input(colorize("Enter a command (add/list/complete/delete/edit/details/search/archive/undo/add_subtask/complete_subtask/quit): ", Fore.CYAN)).lower()
        
        if command == "quit":
            save_tasks(tasks)
            print(colorize("Goodbye!", Fore.YELLOW))
            break
        elif command == "add":
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ")
            due_date = parse_date(due_date_str) if due_date_str else None
            priority_str = input("Enter priority (LOW/MEDIUM/HIGH) or press Enter to skip: ").upper()
            priority = Priority[priority_str] if priority_str in ('LOW', 'MEDIUM', 'HIGH') else None
            category = input("Enter category or press Enter to skip: ")
            add_task(tasks, description, due_date, priority, category)
        elif command == "list":
            sort_option = input("Sort by (due_date/priority) or press Enter for default: ").lower()
            sort_by = sort_option if sort_option in ('due_date', 'priority') else None
            list_tasks(tasks, sort_by)
        elif command == "complete":
            index = int(input("Enter task number to mark as completed: "))
            complete_task(tasks, index)
        elif command == "delete":
            index = int(input("Enter task number to delete: "))
            delete_task(tasks, index)
        elif command == "edit":
            index = int(input("Enter task number to edit: "))
            edit_task(tasks, index)
        elif command == "details":
            index = int(input("Enter task number to show details: "))
            show_task_details(tasks, index)
        elif command == "search":
            keyword = input("Enter keyword to search for: ")
            matching_tasks = search_tasks(tasks, keyword)
            if matching_tasks:
                print(colorize("Matching tasks:", Fore.GREEN))
                for i, task in matching_tasks:
                    print(f"{i}. {task['description']}")
            else:
                print(colorize("No matching tasks found.", Fore.YELLOW))
        elif command == "archive":
            archived_tasks = [task for task in tasks if task['completed']]
            tasks = [task for task in tasks if not task['completed']]
            save_tasks(archived_tasks, 'archived_tasks.json')
            print(colorize(f"{len(archived_tasks)} completed tasks have been archived.", Fore.GREEN))
        elif command == "undo":
            if len(undo_stack) > 0:
                tasks = undo_stack.pop()
                print(colorize("Last action undone.", Fore.GREEN))
            else:
                print(colorize("No actions to undo.", Fore.YELLOW))
        elif command == "add_subtask":
            parent_index = int(input("Enter parent task number: "))
            description = input("Enter subtask description: ")
            add_subtask(tasks, parent_index, description)
        elif command == "complete_subtask":
            parent_index = int(input("Enter parent task number: "))
            subtask_index = int(input("Enter subtask number: "))
            complete_subtask(tasks, parent_index, subtask_index)
        else:
            print(colorize("Invalid command. Please try again.", Fore.RED))

if __name__ == "__main__":
    main()

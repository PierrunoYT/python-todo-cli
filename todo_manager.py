import json
import os
from datetime import datetime, date
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

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

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

def add_task(tasks, description, due_date=None, priority=None, category=None):
    task = {
        "description": description,
        "completed": False,
        "created_at": date.today().isoformat(),
        "due_date": due_date.isoformat() if due_date else None,
        "priority": priority.name if priority else None,
        "category": category
    }
    tasks.append(task)
    print("Task added successfully.")

def list_tasks(tasks, sort_by=None):
    if not tasks:
        print("No tasks found.")
        return

    if sort_by == "due_date":
        sorted_tasks = sorted(tasks, key=lambda x: x["due_date"] or "9999-12-31")
    elif sort_by == "priority":
        priority_order = {None: 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3}
        sorted_tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]], reverse=True)
    else:
        sorted_tasks = tasks

    for i, task in enumerate(sorted_tasks, 1):
        status = "✓" if task["completed"] else " "
        due_date = f" (Due: {task['due_date']})" if task['due_date'] else ""
        priority = f" [Priority: {task['priority']}]" if task['priority'] else ""
        category = f" #{task['category']}" if task['category'] else ""
        print(f"{i}. [{status}] {task['description']}{due_date}{priority}{category}")

def complete_task(tasks, index):
    if 1 <= index <= len(tasks):
        tasks[index-1]["completed"] = True
        print("Task marked as completed.")
    else:
        print("Invalid task number.")

def delete_task(tasks, index):
    if 1 <= index <= len(tasks):
        del tasks[index-1]
        print("Task deleted successfully.")
    else:
        print("Invalid task number.")

def edit_task(tasks, index):
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
    else:
        print("Invalid task number.")

def main():
    tasks = load_tasks()
    
    while True:
        command = input("Enter a command (add/list/complete/delete/edit/details/quit): ").lower()
        
        if command == "quit":
            save_tasks(tasks)
            print("Goodbye!")
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
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

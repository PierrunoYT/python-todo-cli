import json
import os

def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

def add_task(tasks, description):
    task = {"description": description, "completed": False}
    tasks.append(task)
    print("Task added successfully.")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            status = "✓" if task["completed"] else " "
            print(f"{i}. [{status}] {task['description']}")

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

def main():
    tasks = load_tasks()
    
    while True:
        command = input("Enter a command (add/list/complete/delete/quit): ").lower()
        
        if command == "quit":
            save_tasks(tasks)
            print("Goodbye!")
            break
        elif command == "add":
            description = input("Enter task description: ")
            add_task(tasks, description)
        elif command == "list":
            list_tasks(tasks)
        elif command == "complete":
            index = int(input("Enter task number to mark as completed: "))
            complete_task(tasks, index)
        elif command == "delete":
            index = int(input("Enter task number to delete: "))
            delete_task(tasks, index)
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

import json
import random
from datetime import datetime
import os

class Task:
    def __init__(self, title, description, created_at, task_id=None):
        self.title = title
        self.description = description
        self.created_at = created_at
        if task_id:
            self.id = task_id
        else:
            self.id = random.randint(1000, 9999)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at
        }

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    def load_from_file(self):
        try:
            if not os.path.exists(self.filename):
                self.tasks = []
                return

            with open(self.filename, 'r') as file:
                data = json.load(file)
                self.tasks = []
                for task_data in data:
                    new_task = Task(
                        task_data['title'],
                        task_data['description'],
                        task_data['created_at'],
                        task_data['id']
                    )
                    self.tasks.append(new_task)
            print(f"Loaded {len(self.tasks)} tasks from {self.filename}.")
            
        except FileNotFoundError:
            print("No saved tasks found. Starting fresh.")
            self.tasks = []
        except json.JSONDecodeError:
            print("Error reading the file (corrupt JSON). Starting with empty list.")
            self.tasks = []
        except Exception as e:
            print(f"An unexpected error occurred while loading: {e}")

    def save_to_file(self):
        """Saves the current list of tasks to the JSON file."""
        try:
            tasks_data = [task.to_dict() for task in self.tasks]
            
            with open(self.filename, 'w') as file:
                json.dump(tasks_data, file, indent=4)
            
        except IOError as e:
            print(f"Error saving to file: {e}")

    def add_task(self):
        print("\n--- Add New Task ---")
        title = input("Task Title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return

        description = input("Description: ").strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_task = Task(title, description, created_at)
        self.tasks.append(new_task)
        self.save_to_file()
        print("Task added successfully!")

    def view_tasks(self):
        print("\n--- Your Tasks ---")
        if not self.tasks:
            print("No tasks found.")
            return

        for index, task in enumerate(self.tasks, start=1):
            print(f"{index}. [ID: {task.id}] {task.title}")
            print(f"   Description: {task.description}")
            print(f"   Created: {task.created_at}")
            print("-" * 30)

    def update_task(self):
        self.view_tasks()
        if not self.tasks:
            return

        try:
            choice = int(input("\nEnter the number of the task to update: "))
            if 1 <= choice <= len(self.tasks):
                task = self.tasks[choice - 1]
                
                print(f"Updating '{task.title}' (Leave blank to keep current)")
                
                new_title = input(f"New Title [{task.title}]: ").strip()
                if new_title:
                    task.title = new_title
                
                new_desc = input(f"New Description [{task.description}]: ").strip()
                if new_desc:
                    task.description = new_desc
                
                self.save_to_file()
                print("Task updated successfully!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return

        try:
            choice = int(input("\nEnter the number of the task to delete: "))
            if 1 <= choice <= len(self.tasks):
                removed_task = self.tasks.pop(choice - 1)
                self.save_to_file()
                print(f"Task '{removed_task.title}' deleted successfully!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    manager = TaskManager()

    while True:
        print("\n===== Student Task Tracker =====")
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Enter choice: ").strip()

        if choice == '1':
            manager.add_task()
        elif choice == '2':
            manager.view_tasks()
        elif choice == '3':
            manager.update_task()
        elif choice == '4':
            manager.delete_task()
        elif choice == '5':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()

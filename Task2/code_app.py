# ============================================
# Alternative Console To-Do Application
# Using Class-Based Approach
# ============================================

class TodoApp:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    # -----------------------------
    # Load tasks from file
    # -----------------------------
    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                self.tasks = file.read().splitlines()
        except FileNotFoundError:
            # File will be created automatically later
            self.tasks = []

    # -----------------------------
    # Save tasks to file
    # -----------------------------
    def save_tasks(self):
        with open(self.filename, "w") as file:
            file.write("\n".join(self.tasks))

    # -----------------------------
    # Display tasks
    # -----------------------------
    def show_tasks(self):
        print("\n----- YOUR TASKS -----")
        if not self.tasks:
            print("No tasks found.")
        else:
            for i in range(len(self.tasks)):
                print(f"{i+1}. {self.tasks[i]}")
        print("----------------------")

    # -----------------------------
    # Add task
    # -----------------------------
    def add_task(self):
        task = input("Enter task: ").strip()
        if task:
            self.tasks.append(task)
            self.save_tasks()
            print("Task added ✔")
        else:
            print("Task cannot be empty!")

    # -----------------------------
    # Delete task
    # -----------------------------
    def delete_task(self):
        self.show_tasks()
        if self.tasks:
            try:
                num = int(input("Enter task number to delete: "))
                removed = self.tasks.pop(num - 1)
                self.save_tasks()
                print(f"Deleted: {removed}")
            except (ValueError, IndexError):
                print("Invalid number!")

    # -----------------------------
    # Main menu loop
    # -----------------------------
    def run(self):
        while True:
            print("\n====== TO-DO MENU ======")
            print("1. Show Tasks")
            print("2. Add Task")
            print("3. Delete Task")
            print("4. Exit")

            choice = input("Choose option: ")

            if choice == "1":
                self.show_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice!")


# -----------------------------
# Start Application
# -----------------------------
if __name__ == "__main__":
    app = TodoApp()
    app.run()

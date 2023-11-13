import tkinter as tk
from tkinter import ttk, messagebox, font
from db import create_connection, add_task, update_task, delete_task, get_all_tasks

class TaskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Task Scheduler")
        self.root.geometry("1300x800")  # Adjust the size of the window
        self.root.configure(bg='#f0f0f0')  # Set a background color

        # Custom font
        self.custom_font = font.Font(family="Helvetica", size=10)

        # Create Widgets
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        labels = ['Title', 'Description', 'Deadline (YYYY-MM-DD)', 'Priority', 'Status']
        self.entries = {}
        for idx, label in enumerate(labels):
            tk.Label(frame, text=label, bg='#f0f0f0', font=self.custom_font).grid(row=idx, column=0, padx=10, pady=5)
            entry = tk.Entry(frame, font=self.custom_font)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label] = entry

        # Buttons with different colors
        tk.Button(frame, text="Add Task", command=self.add_task, bg='#4CAF50', fg='white', font=self.custom_font).grid(row=6, column=0, padx=10, pady=10)
        tk.Button(frame, text="Update Selected Task", command=self.update_selected_task, bg='#FFC107', fg='black', font=self.custom_font).grid(row=6, column=1, padx=10, pady=10)
        tk.Button(frame, text="Delete Selected Task", command=self.delete_selected_task, bg='#F44336', fg='white', font=self.custom_font).grid(row=7, column=0, padx=10, pady=10)
        tk.Button(frame, text="Refresh List", command=self.refresh_tasks, bg='#2196F3', fg='white', font=self.custom_font).grid(row=7, column=1, padx=10, pady=10)

        # Treeview for Task Display
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Title', 'Description', 'Deadline', 'Priority', 'Status'), show='headings')
        self.tree.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.refresh_tasks()

    def add_task(self):
        task_details = [self.entries[label].get() for label in self.entries]
        conn = create_connection("tasks.db")
        add_task(conn, task_details)
        conn.close()
        self.refresh_tasks()

    def update_selected_task(self):
        selected_item = self.tree.selection()[0]
        selected_task = self.tree.item(selected_item, 'values')
        task_details = [self.entries[label].get() for label in self.entries]
        task_details.append(selected_task[0])  # Append the task ID for updating

        conn = create_connection("tasks.db")
        update_task(conn, task_details)
        conn.close()
        self.refresh_tasks()

    def delete_selected_task(self):
        selected_item = self.tree.selection()[0]
        task_id = self.tree.item(selected_item, 'values')[0]

        response = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this task?")
        if response:
            conn = create_connection("tasks.db")
            delete_task(conn, task_id)
            conn.close()
            self.refresh_tasks()

    def refresh_tasks(self):
        # Clear the current items in the tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Add tasks to the tree
        conn = create_connection("tasks.db")
        tasks = get_all_tasks(conn)
        for task in tasks:
            self.tree.insert('', 'end', values=task)
        conn.close()

def main():
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()

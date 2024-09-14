import tkinter as tk

class UserDisplay:
    def __init__(self, users):
        self.window = tk.Toplevel()
        self.window.title("All Users")
        
        if users:
            user_list = "\n".join([f"User ID: {user.user_id}, Name: {user.name}, Borrowed Books: {len(user.borrowed_books)}" for user in users])
            tk.Label(self.window, text=user_list, justify=tk.LEFT).pack(pady=10)
        else:
            tk.Label(self.window, text="No users registered", justify=tk.LEFT).pack(pady=10)

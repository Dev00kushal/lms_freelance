import tkinter as tk
from tkinter import messagebox

class BookDisplay:
    def __init__(self, books):
        self.window = tk.Toplevel()
        self.window.title("All Books")
        
        if books:
            book_list = "\n".join([f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {'Yes' if not book.is_borrowed else 'No'}" for book in books])
            tk.Label(self.window, text=book_list, justify=tk.LEFT).pack(pady=10)
        else:
            tk.Label(self.window, text="No books available", justify=tk.LEFT).pack(pady=10)

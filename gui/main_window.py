import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

from models.book import Book
from models.library import Library
from models.user import User

class MainWindow:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.setup_ui()

    def setup_ui(self):
        style = ttkb.Style(theme="flatly")
        self.root.configure(bg=style.colors.bg)
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        main_frame = ttkb.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = ttkb.Label(main_frame, text="Library Management System", 
                                  font=("Helvetica", 24, "bold"), bootstyle="inverse-primary")
        header_label.pack(pady=(0, 20), fill=X)

        self.notebook = ttkb.Notebook(main_frame, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)

        self.book_frame = ttkb.Frame(self.notebook, padding="20")
        self.user_frame = ttkb.Frame(self.notebook, padding="20")
        self.borrow_frame = ttkb.Frame(self.notebook, padding="20")

        self.notebook.add(self.book_frame, text="Book Management")
        self.notebook.add(self.user_frame, text="User Management")
        self.notebook.add(self.borrow_frame, text="Borrow & Return")

        self.setup_book_management()
        self.setup_user_management()
        self.setup_borrow_return()

        # Footer with credit
        footer_label = ttkb.Label(self.root, text="Made with Ankit Limbu", 
                                  font=("Helvetica", 12), bootstyle="light")
        footer_label.pack(side=BOTTOM, pady=10)

    def setup_book_management(self):
        input_frame = ttkb.Frame(self.book_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.book_entries = self.create_section(input_frame, "Book Title:", "Author:", "ISBN:")
        ttkb.Button(input_frame, text="Add Book", command=lambda: self.add_book(self.book_entries), 
                    bootstyle="success").pack(pady=10)

        ttkb.Button(self.book_frame, text="Show Books", command=self.show_books, 
                    bootstyle="info").pack(pady=10)

    def setup_user_management(self):
        input_frame = ttkb.Frame(self.user_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.user_entries = self.create_section(input_frame, "User ID:", "Name:")
        ttkb.Button(input_frame, text="Register User", command=lambda: self.add_user(self.user_entries), 
                    bootstyle="success").pack(pady=10)

        ttkb.Button(self.user_frame, text="Show Users", command=self.show_users, 
                    bootstyle="info").pack(pady=10)

    def setup_borrow_return(self):
        input_frame = ttkb.Frame(self.borrow_frame)
        input_frame.pack(fill=X, pady=(0, 20))

        self.borrow_entries = self.create_section(input_frame, "User ID:", "Book ISBN:")
        ttkb.Button(input_frame, text="Borrow Book", command=lambda: self.borrow_book(self.borrow_entries), 
                    bootstyle="success").pack(side=LEFT, padx=(0, 10))
        ttkb.Button(input_frame, text="Return Book", command=self.return_book, 
                    bootstyle="warning").pack(side=LEFT)

        ttkb.Button(self.borrow_frame, text="Show Borrowed Books", command=self.show_borrowed_books, 
                    bootstyle="info").pack(pady=10)

    def create_section(self, parent_frame, *labels):
        entries = {}
        for i, label_text in enumerate(labels):
            frame = ttkb.Frame(parent_frame)
            frame.pack(fill=X, pady=5)
            ttkb.Label(frame, text=label_text, width=10).pack(side=LEFT)
            entry = ttkb.Entry(frame, font=("Helvetica", 10))
            entry.pack(side=LEFT, expand=YES, fill=X)
            entries[f'entry{i+1}'] = entry
        return entries

    def add_book(self, entries):
        title = entries['entry1'].get()
        author = entries['entry2'].get()
        isbn = entries['entry3'].get()
        
        if title and author and isbn:
            book = Book(title, author, isbn)
            self.library.add_book(book)
            self.show_success_animation("Book added successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_books()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def add_user(self, entries):
        user_id = entries['entry1'].get()
        name = entries['entry2'].get()
        
        if user_id and name:
            user = User(user_id, name)
            self.library.add_user(user)
            self.show_success_animation("User registered successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_users()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    def borrow_book(self, entries):
        user_id = entries['entry1'].get()
        isbn = entries['entry2'].get()
        
        if self.library.borrow_book(user_id, isbn):
            self.show_success_animation("Book borrowed successfully!")
            for entry in entries.values():
                entry.delete(0, tk.END)
            self.refresh_borrowed_books()
        else:
            messagebox.showwarning("Error", "Book could not be borrowed. Check User ID or ISBN.")

    def return_book(self):
        user_id = self.borrow_entries['entry1'].get()
        isbn = self.borrow_entries['entry2'].get()
        
        if self.library.return_book(user_id, isbn):
            self.show_success_animation("Book returned successfully!")
            self.refresh_borrowed_books()
        else:
            messagebox.showwarning("Error", "Book could not be returned. Check User ID or ISBN.")

    def refresh_books(self):
        books = self.library.get_books()
        self.books_listbox.delete(0, tk.END)
        for book in books:
            self.books_listbox.insert(tk.END, f"{book.title} by {book.author} (ISBN: {book.isbn})")

    def refresh_users(self):
        users = self.library.get_users()
        self.users_listbox.delete(0, tk.END)
        for user in users:
            self.users_listbox.insert(tk.END, f"{user.user_id}: {user.name}")

    def refresh_borrowed_books(self):
        borrowed_books = self.library.get_borrowed_books()
        self.borrowed_books_listbox.delete(0, tk.END)
        for isbn, user_id in borrowed_books.items():
            book = self.library.get_book_by_isbn(isbn)  # Assuming this method exists
            book_name = book.title if book else "Unknown"
            user = self.library.get_user_by_id(user_id)  # Assuming this method exists
            user_name = user.name if user else "Unknown"
            self.borrowed_books_listbox.insert(tk.END, f"Book: {book_name}, ISBN: {isbn}, User: {user_name}")

    def show_books(self):
        self.show_table_window("Books", ["Title", "Author", "ISBN"], 
                               [(b.title, b.author, b.isbn) for b in self.library.get_books()])
    
    def show_users(self):
        self.show_table_window("Users", ["User ID", "Name"], 
                               [(u.user_id, u.name) for u in self.library.get_users()])
    
    def show_borrowed_books(self):
        borrowed_books = self.library.get_borrowed_books()
        data = []
        for isbn, user_id in borrowed_books.items():
            book = self.library.get_book_by_isbn(isbn)
            book_name = book.title if book else "Unknown"
            user = self.library.get_user_by_id(user_id)
            user_name = user.name if user else "Unknown"
            data.append((book_name, isbn, user_name))
        self.show_table_window("Borrowed Books", ["Book Name", "ISBN", "User"], data)

    def show_table_window(self, title, columns, data):
        table_window = tk.Toplevel(self.root)
        table_window.title(title)
        table_window.geometry("600x400")

        search_frame = ttkb.Frame(table_window, padding="10")
        search_frame.pack(fill=X, padx=20)

        search_label = ttkb.Label(search_frame, text="Search:")
        search_label.pack(side=LEFT)

        search_var = tk.StringVar()
        search_entry = ttkb.Entry(search_frame, textvariable=search_var, font=("Helvetica", 12))
        search_entry.pack(side=LEFT, fill=X, expand=YES)

        filter_button = ttkb.Button(search_frame, text="Filter", command=lambda: self.filter_table(tree, search_var.get()))
        filter_button.pack(side=LEFT, padx=10)

        tree = ttk.Treeview(table_window, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=YES, padx=20, pady=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.W)

        for row in data:
            tree.insert('', tk.END, values=row)

    def filter_table(self, tree, search_text):
        for item in tree.get_children():
            tree.delete(item)
        
        data = [(b.title, b.author, b.isbn) for b in self.library.get_books() if search_text.lower() in b.title.lower()]
        for row in data:
            tree.insert('', tk.END, values=row)

    def show_success_animation(self, message):
        success_window = ttkb.Toplevel(self.root)
        success_window.overrideredirect(True)
        success_window.attributes("-alpha", 0.0)
        success_window.geometry(f"+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")

        frame = ttkb.Frame(success_window, padding=20)
        frame.pack()

        label = ttkb.Label(frame, text=message, font=("Helvetica", 16))
        label.pack()

        def fade_in():
            alpha = success_window.attributes("-alpha")
            if alpha < 1.0:
                success_window.attributes("-alpha", alpha + 0.1)
                success_window.after(50, fade_in)
            else:
                success_window.after(1000, fade_out)

        def fade_out():
            alpha = success_window.attributes("-alpha")
            if alpha > 0.0:
                success_window.attributes("-alpha", alpha - 0.1)
                success_window.after(50, fade_out)
            else:
                success_window.destroy()

        fade_in()
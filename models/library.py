class Library:
    def __init__(self):
        self.books = []  # List to store book instances
        self.users = []  # List to store user instances
        self.borrowed_books = {}  # Dictionary to track borrowed books

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def borrow_book(self, user_id, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if isbn not in self.borrowed_books:
                    self.borrowed_books[isbn] = user_id
                    return True
        return False

    def return_book(self, user_id, isbn):
        if isbn in self.borrowed_books and self.borrowed_books[isbn] == user_id:
            del self.borrowed_books[isbn]
            return True
        return False

    def get_books(self):
        return self.books

    def get_users(self):
        return self.users

    def get_borrowed_books(self):
        return self.borrowed_books

    def get_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

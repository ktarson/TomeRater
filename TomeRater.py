
# coding: utf-8

# In[1]:


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {} 
        
    def __hash__(self):
        return hash((self.name, self.email))

    def get_email(self):
        return self.email

    def change_email(self, address):
        print("This user's email has been updated to {}".format(address))
        self.email = address

    def __repr__(self):
        output = "User: {name}, email: {email}, books read: {books}".format(name=self.name, email=self.email, books=len(self.books))
        return output

    def __eq__(self, other_user):
        super().__eq__(self, other_user)
        return self.user == other_user
        
    def read_book(self, book, rating=None):
        self.books[book] = rating
        
    def get_average_rating(self): # only accounts for books that have a rating
        total_rating = 0
        books_rated = 0
        for book in self.books:
            if self.books[book] == None:
                pass
            else:
                total_rating += self.books[book]
                books_rated += 1
        return total_rating / books_rated
        
class Book:
    def __init__(self, title, isbn):
        self.title = str(title)
        self.isbn = isbn
        self.ratings = []
        
    def __repr__(self):
        return "{title}".format(title=self.title)
    
    def get_title(self):
        return self.title
        
    def get_isbn(self):
        return self.isbn
        
    def set_isbn(self, new):
        self.isbn = new
        print("{title}'s ISBN ({old}) has been updated to {new}.".format(title=self.title,old=self.isbn, new=new))
        
    def add_rating(self, rating):
        if (rating >= 0) and (rating <= 4):
            self.ratings.append(rating)
        else:
            print("Invalid Rating.")

    def __eq__(self,other_book):
        super().__eq__(self, other_book)
        return self.book == other_book
        
    def get_average_rating(self):
        total = 0
        count = 0
        for x in self.ratings:
            total += self.ratings[count]
            count += 1
        return round(total / len(self.ratings), 2)
        
    def __hash__(self):
        return hash((self.title, self.isbn))
        
        
class Fiction(Book):
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.ratings = []
    
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)
    
    def get_author(self, author):
        return self.author

class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        self.title = title
        self.subject = str(subject)
        self.level = str(level)
        self.isbn = isbn
        self.ratings = []
        
    def __repr__(self):
        return "{title}, a(n) {level}-level manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)
    
    def get_subject(self):
        return self.subject
        
    def get_level(self):
        return self.level
        
class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
        
    def get_isbns(self):
        isbns = [book.get_isbn() for book in self.books]
        return list(isbns)
 
    def create_book(self, title, isbn):
        if isbn in list(self.get_isbns()):
            print("ISBN already exists.")
        else:
            return Book(title, isbn)
    
    def create_novel(self, title, author, isbn):
        if isbn in list(self.get_isbns()):
            print("ISBN already exists.")
        else:
            return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        if isbn in list(self.get_isbns()):
            print("ISBN already exists.")
        else:
            return NonFiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        try:
            self.users[email].read_book(book, rating)
            if rating:
                book.add_rating(rating)   
            try:
                self.books[book] += 1
            except:
                self.books[book] = 1  
        except:    
            print("No user with that email.")        

    def add_user(self, name, email, user_books=None):
        if email in self.users:
            print("This user already exists.")
        else:
            if ('@' in email) and ('.com' in email or '.edu' in email or '.org' in email):
                self.users[email] = User(name, email)
                if user_books:
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Invalid email address.")
    
    def print_catalog(self):
        for book in self.books:
            print(book)
    
    def print_users(self):
        for user in self.users:
            print(user)
            
    def get_most_read_book(self):
        most_read = 0
        book_read = ''
        for book in self.books:
            if self.books[book] > most_read:
                most_read = self.books[book]
                book_read = book
        return book_read
    
    def highest_rated_book(self):
        highest_avg = 0
        highest_book = ''
        for book in self.books:
            if book.get_average_rating() > highest_avg:
                highest_avg = book.get_average_rating()
                highest_book = book
        return highest_book
    
    def most_positive_user(self):
        highest_avg = 0
        highest_user = ''
        for user in self.users:
            if self.users[user].get_average_rating() > highest_avg:
                highest_avg = self.users[user].get_average_rating()
                highest_user = self.users[user]
        return highest_user            
    
    def get_n_most_read_books(self, n):
        full_books_list = dict(self.books)
        most_read_list = []
        book_pop = None
        while n > 0 and len(full_books_list) > 0:
            most_read_num = 0           
            most_read_book = None
            for book in full_books_list:
                if full_books_list[book] >= most_read_num:
                    most_read_num = full_books_list[book]
                    most_read_book = book
                    book_pop = book
            most_read_list.append(most_read_book.title)
            full_books_list.pop(book_pop)
            n -= 1
        return most_read_list
    
    def get_n_most_prolific_readers(self, n):
        full_users = dict(self.users)
        prolific_users = []
        user_pop = None
        while n > 0 and len(full_users) > 0:
            most_read_books = 0
            most_prolific_user = None
            for user in full_users:
                if len(full_users[user].books) >= most_read_books:
                    most_read_books = len(full_users[user].books)
                    most_prolific_user = user
                    user_pop = user
            prolific_users.append(most_prolific_user)
            full_users.pop(user_pop)
            n -= 1
        return prolific_users
    
    def __print__(self):
        print("Welcome to Tome Rater.")
        print("Users: ")
        for user in self.users:
            print(user)

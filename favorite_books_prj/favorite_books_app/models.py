from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if 'first_name' not in postData or len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters."
        if 'last_name' not in postData or len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        email_usage = self.filter(email = postData['email'])
        if email_usage:
            errors['email'] = "Email already exists"
        if 'password' not in postData or len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "The passwords do not match!"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email = email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw
        )

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if 'title' not in postData or len(postData['title']) < 1 :
            errors['title'] = "A title is required"
        if 'desc' not in postData or len(postData['desc']) < 5:
            errors['desc'] = "A description should be 5 characters and more."
        return errors
        
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    uploaded_by_id = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

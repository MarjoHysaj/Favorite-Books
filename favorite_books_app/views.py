from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.core.exceptions import PermissionDenied

def index(request):
    if "user_id" in request.session:
        return redirect('/books')
    return render(request, "index.html")

def login(request):
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request,value)
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/books')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/books')

def logout(request):
    request.session.flush()
    return redirect('/')

def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user':user,
        'books':Book.objects.all()
    }
    return render(request, 'books.html', context)

def bookCreate(request):
    errors = Book.objects.book_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.create(
            title=request.POST['title'],
            desc=request.POST['desc'],
            uploaded_by_id=user
        )
        user.liked_books.add(book)
        return redirect('/books')

def showBook(request, book_id):
    context = {
        'book' : Book.objects.get(id=book_id),
        'this_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "showbook.html", context)

def updateBook(request, book_id):
    book = Book.objects.get(id=book_id)
    book.desc = request.POST['desc']
    book.save()
    return redirect(f'/books/{book.id}/show')

def deleteBook(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')

def favorite(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.add(book)
    return redirect(f'/books/{book.id}/show')

def remove(request, book_id):
    user = User.objects.get(id=request.session['user_id'])
    book = Book.objects.get(id=book_id)
    user.liked_books.remove(book)
    return redirect(f'/books/{book.id}/show')

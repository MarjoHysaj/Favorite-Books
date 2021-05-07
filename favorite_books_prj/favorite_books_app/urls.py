from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('books', views.books),
    path('books/create', views.bookCreate),
    path('books/<int:book_id>/show', views.showBook),
    path('books/<int:book_id>/update', views.updateBook),
    path('books/<int:book_id>/delete', views.deleteBook),
    path('favorite/<int:book_id>', views.favorite),
    path('remove/<int:book_id>', views.remove)
]

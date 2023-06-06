from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    #path('ratings', views.RatingsView.as_view()),
    #path('books/', views.books),
    #to map all the class as a view
    #path('books', views.BookList.as_view()),
    #path('books/<int:pk>', views.Book.as_view()),    
    path('menu-items', views.MenuItemView.as_view()),  

]
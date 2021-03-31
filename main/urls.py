
from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('adduser', AddUser.as_view()),
    path('change-password', ChangePassword.as_view()),
    path('delete-user/<int:id>', DeleteUser.as_view()),
    path('edit-user/<int:id>', EditUser.as_view()),
    path('logout', LogoutView.as_view()),
]

from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

from django.views import View
from django.contrib.auth.models import User, auth


class IndexView(View):
    def get(self, request):
        if(not request.user.is_authenticated):
            return redirect('/login')
        users = User.objects.all()
        return render(request, "index.html", {"users": users})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')


class LoginView(View):
    def get(self, request):
        if(request.user.is_authenticated):
            return redirect('/')
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        error = 0
        if(username == ""):
            messages.add_message(request, messages.ERROR,
                                 "Username can't be empty.")
            error += 1
        if(password == ""):
            messages.add_message(request, messages.ERROR,
                                 "Password can't be empty.")
            error += 1

        if(not error):
            user = auth.authenticate(
                request, username=username, password=password)

            if(user is not None):
                auth.login(request, user)
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR,
                                     "Username or Password was wrong")

        return redirect('/login')


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        error = 0
        if(email == ""):
            messages.add_message(request, messages.ERROR,
                                 "Email can't be empty.")
            error += 1
        if(password == ""):
            messages.add_message(request, messages.ERROR,
                                 "Password can't be empty.")
            error += 1
        if(User.objects.filter(username=email).exists()):
            messages.add_message(request, messages.ERROR,
                                 "Email already registered.")
            error += 1

        if(not error):
            user = User.objects.create_user(
                username=email, password=password, email=email, first_name=first_name, last_name=last_name,)
            if user is not None:
                user.set_password(password)
                user = auth.authenticate(
                    request, username=email, password=password)
                auth.login(request, user)
                return redirect('/')

        return redirect('/register')


class AddUser(View):
    def post(self, request):
        if not request.user.is_superuser:
            messages.add_message(request, messages.ERROR,
                                 "You can't add user.")
            return redirect('/')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        error = 0
        if(email == ""):
            messages.add_message(request, messages.ERROR,
                                 "Email can't be empty.")
            error += 1
        if(password == ""):
            messages.add_message(request, messages.ERROR,
                                 "Password can't be empty.")
            error += 1
        if(User.objects.filter(username=email).exists()):
            messages.add_message(request, messages.ERROR,
                                 "Email already registered.")
            error += 1

        if(not error):
            user = User.objects.create_user(
                username=email, password=password, email=email, first_name=first_name, last_name=last_name,)
            if user is not None:
                user.set_password(password)
                messages.add_message(request, messages.SUCCESS,
                                     "User added successfully!")
                return redirect('/')
        return redirect('/')


class DeleteUser(View):
    def get(self, request, id=None):
        if not request.user.is_superuser and request.user.id != id:
            messages.add_message(request, messages.ERROR,
                                 "You can't delete this user.")
            return redirect('/')

        user = User.objects.get(id=id)
        if(user is not None):
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 "User deleted.")
        else:
            messages.add_message(request, messages.ERROR,
                                 "No user found.")
            return redirect('/')
        if(id == request.user.id):
            auth.logout(request)

        return redirect('/')


class EditUser(View):
    def get(self, request, id=None):
        if not request.user.is_superuser and request.user.id != id:
            messages.add_message(request, messages.ERROR,
                                 "You can't edit this user.")
            return redirect('/')
        user = User.objects.get(id=id)
        return render(request, "edit.html", {"user": user})

    def post(self, request, id=None):
        if not request.user.is_superuser and request.user.id != id:
            messages.add_message(request, messages.ERROR,
                                 "You can't edit this user.")
            return redirect('/')

        user = User.objects.get(id=id)
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        #email = request.POST.get('email')
        user.first_name = first_name
        user.last_name = last_name
        #user.email = email
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             "User details updated.")
        if request.user.id == id:
            messages.add_message(request, messages.WARNING,
                                 "Please relogin to change those effect.")

        return redirect('/')


class ChangePassword(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 "You aren't loged in.")
            return redirect('/')

        return render(request, "changepassword.html")

    def post(self, request):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR,
                                 "You aren't loged in.")
            return redirect("/")
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        user = User.objects.get(id=request.user.id)
        error = 0

        if(len(newpass) < 8):
            messages.add_message(request, messages.ERROR,
                                 "New password cant be less than 8 charecture.")
            error += 1

        if error:
            return redirect('/change-password')

        if(user.check_password(oldpass)):
            user.set_password(newpass)
            user.save()
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 "Password updated.")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Old Password doesn't match.")

        return redirect('/change-password')

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .models import CustomUser
import django.contrib.auth as i


def dosignup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        if (password != conpassword):
            con1 = {'error_signup': 'password not matching'}
            return render(request, 'index.html', con1)

        if existUser(email):
            con1 = {'error_signup': 'This email already exist.'}
            return render(request, 'index.html', con1)
        else:
            # sign up
            user = CustomUser.objects.create_user(name=name, email=email, password=password, user_type='local')
            user.save()

            # auto login after signup
            user1 = i.authenticate(email=email, password=password)
            if user1 is not None:
                i.login(request, user1)
                return redirect('/home')
            else:
                con1 = {'error_signup': 'some error'}

        return render(request, 'index.html', con1)
    else:
        return redirect('/')


def dosignin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = i.authenticate(email=email, password=password)
        if user is not None:
            i.login(request, user)
            return redirect('/home')
        else:
            con1 = {'error_login': 'Wrong email or password.'}
            return render(request, 'index.html', con1)

    else:
        if request.user.is_authenticated:
            return redirect('/home')
        return redirect('/')


def gohome(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'index.html')


def existUser(user):
    try:
        u = CustomUser.objects.get(email=user)
        return True
    except CustomUser.DoesNotExist:
        return False


def logout(request):
    i.logout(request)
    return redirect('/')

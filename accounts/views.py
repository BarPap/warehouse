from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

def login_view(request):
    errors = {}

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username:
            errors['username'] = 'Nazwa nie może być pusta'
        elif not password:
            errors['password'] = 'Hasło nie może być puste'

        if not errors:
            user = authenticate(request, username=username, password=password)
        else:
            return render(request, 'accounts/login.html', {"errors": errors})

        if user:
            login(request, user)
            return redirect('/products/')
        else:
            return render(request, 'accounts/login.html', {"errors": errors})

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login/')
    return redirect('/products/')
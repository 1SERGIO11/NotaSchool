from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            user = form.save()
            auth_login(request, user)
            return JsonResponse({"success": True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "errors": errors})
    else:
        form = RegisterForm()
    return render(request, 'Регистрация.html', {'form': form})

def check_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

def home(request):
    return render(request, 'Главная.html')

def check_email(request):
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(response)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return JsonResponse({"success": False, "errors": "Неверное имя пользователя или пароль"})
    else:
        return render(request, 'Вход.html')
def courses_view(request):
    """
    Представление для страницы курсов.
    """
    return render(request, 'Курсы.html')

def blog_view(request):
    """
    Представление для страницы блога.
    """
    return render(request, 'Блог.html')

def analysis_view(request):
    """
    Представление для страницы 'Разборы'.
    """
    return render(request, 'Разборы.html')
def user_home(request):
    return render(request, 'user_home.html')

def profile(request):
    # Здесь можно добавить логику, например, проверку авторизации пользователя
    return render(request, 'Профиль.html')
def player_view(request):
    # Логика для страницы 'Плеер.html', если она вам нужна
    return render(request, 'Плеер.html')
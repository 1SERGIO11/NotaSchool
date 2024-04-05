from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Video, Comment, ViewHistory
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from django.db import IntegrityError


def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, pk=video_id)
        comment_text = request.POST.get('comment')
        if comment_text:  # Добавьте проверку, что комментарий не пустой
            Comment.objects.create(video=video, user=request.user, comment_text=comment_text)
            return redirect('player', video_id=video_id)
    # Если метод запроса не POST или комментарий пустой, перенаправьте пользователя обратно на страницу видео
    return redirect('player', video_id=video_id)
def get_word_form(number, form_for_1, form_for_2, form_for_5):
    number = abs(number) % 100
    if number > 10 and number < 20:
        return form_for_5
    number = number % 10
    if number == 1:
        return form_for_1
    if number > 1 and number < 5:
        return form_for_2
    return form_for_5

def get_comment_form(number):
    number = abs(number) % 100
    if 5 <= number <= 20:
        return 'комментариев'
    number = number % 10
    if number == 1:
        return 'комментарий'
    if 2 <= number <= 4:
        return 'комментария'
    return 'комментариев'

def player_view(request, video_id):
    # Основное видео, которое пользователь хочет посмотреть
    video = get_object_or_404(Video, pk=video_id)

    # Получаем другие видео для отображения на странице
    # Например, последние 5 видео, исключая текущее
    other_videos = Video.objects.exclude(id=video_id).order_by('-creation_date')[:5]

    if request.user.is_authenticated:
        user = request.user
        if not ViewHistory.objects.filter(user=user, video=video).exists():
            ViewHistory.objects.create(user=user, video=video, view_date=timezone.now())
            Video.objects.filter(pk=video_id).update(view_count=F('view_count') + 1)
            video.refresh_from_db()

    view_form = get_word_form(video.view_count, "просмотр", "просмотра", "просмотров")
    comments = video.comments.all()

    # Подсчет количества комментариев и определение их формы
    comments_count = comments.count()
    comments_form = get_word_form(comments_count, "комментарий", "комментария", "комментариев")

    # Передаем в шаблон и основное видео, и список других видео
    return render(request, 'Плеер.html', {
        'video': video,
        'comments': comments,
        'view_form': view_form,
        'comments_count': comments_count,
        'comments_form': comments_form,
        'other_videos': other_videos,  # Добавляем другие видео в контекст
    })

def analysis_page(request):
    videos = Video.objects.all()  # Получаем все видео из базы данных

    # Для каждого видео добавляем форму слова "просмотр" в зависимости от количества
    for video in videos:
        video.views_word = get_word_form(video.view_count, "просмотр", "просмотра", "просмотров")

    return render(request, 'Разборы.html', {'videos': videos})





def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'Регистрация.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return JsonResponse({"success": True, "redirect": "/"})
            except IntegrityError as e:
                return JsonResponse({"success": False, "errors": "Это имя пользователя уже занято."}, status=400)
        else:
            # Сбор ошибок формы для отображения на клиенте
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "errors": errors}, status=400)


def check_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

def home(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Если пользователь авторизован, перенаправляем его на страницу авторизированного пользователя
        return redirect('user_home')
    else:
        # Если пользователь не авторизован, отображаем главную страницу
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

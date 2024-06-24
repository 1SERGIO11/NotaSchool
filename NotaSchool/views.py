from .forms import RegisterForm, UserUpdateForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Video, Comment, ViewHistory, UserProfile, LikedVideo
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)


def add_like(request, video_id):
    if not request.user.is_authenticated:
        # Возвращаем JSON-ответ с кодом 401, когда пользователь не авторизован
        return JsonResponse({'error': 'Authentication required'}, status=401)

    video = get_object_or_404(Video, pk=video_id)

    # Проверяем, ставил ли уже пользователь лайк на это видео
    if LikedVideo.objects.filter(user=request.user, video=video).exists():
        # Если лайк уже есть, возвращаем ошибку
        return JsonResponse({'error': 'You have already liked this video'}, status=400)

    # Если лайка не было, создаем лайк
    LikedVideo.objects.create(user=request.user, video=video)
    video.like_count = F('like_count') + 1
    video.save()
    video.refresh_from_db()  # Обновляем объект для получения нового значения like_count

    # Возвращаем количество лайков в JSON-формате
    return JsonResponse({'likes': video.like_count})
def course_view(request):
    return render(request, 'Курс-1.html')

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





from django.db import transaction

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'Регистрация.html', {'form': form})
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Обеспечивает атомарность операции
                    user = form.save()  # Сохраняем пользователя
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Входим в систему
                    return JsonResponse({"success": True, "redirect": "/"})  # Перенаправляем на главную
            except IntegrityError as e:
                logger.error(f"Ошибка при регистрации: {e}")  # Логируем ошибку
                # Проверяем сообщение об ошибке, чтобы уточнить её природу
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    error_message = "Это имя пользователя уже занято."
                else:
                    error_message = "Произошла ошибка при регистрации."
                return JsonResponse({"success": False, "errors": error_message}, status=400)
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

@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
        logger.debug('Profile data: %s', profile.__dict__)
    except User.profile.RelatedObjectDoesNotExist:
        profile = UserProfile.objects.create(user=user)
        logger.debug('New profile created')
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'Профиль.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm
from django.urls import reverse
from .models import GlobalNotification
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, Profile
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone
User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()


            GlobalNotification.objects.create(
                message=f"Новый покупатель {user.username} присоединился!",
                created_at=timezone.now()
            )
            login(request, user)

            # ✅ Отправляем сообщение по WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "users",
                {
                    "type": "send_user_notification",
                    "message": f"Зарегистрирован новый пользователь: {user.username}"
                }
            )
            messages.success(request, 'Регистрация прошла успешно!')

            return redirect(reverse('product_list'))
        else:
            messages.error(request, 'Ошибка регистрации. Пожалуйста, проверьте введенные данные.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    message = ''
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                login(request, user)
                if user.is_superuser:
                    return redirect('product_list')
                else:
                    return redirect('product_list')
            else:
                message = 'Неверный логин или пароль'
    return render(request, 'login.html', {'form': form, 'message': message})

def profile(request):
    return render(request, 'profile.html', {'user': request.user})



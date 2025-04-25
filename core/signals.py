from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import GlobalNotification  # Импортируем модель уведомлений

@receiver(post_save, sender=User)
def create_user_notification(sender, instance, created, **kwargs):
    if created:  # Только если пользователь был создан (не обновлён)
        # Создаём уведомление
        GlobalNotification.objects.create(
            title="Новый пользователь",
            message=f"Пользователь {instance.username} зарегистрировался на сайте."
        )

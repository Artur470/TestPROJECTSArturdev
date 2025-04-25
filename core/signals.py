from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from core.models import GlobalNotification

@receiver(post_save, sender=User)
def create_user_notification(sender, instance, created, **kwargs):
    if created:

        GlobalNotification.objects.create(
            title="Новый пользователь",
            message=f"Пользователь {instance.username} зарегистрировался на сайте."
        )

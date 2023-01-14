from allauth.account.signals import email_confirmed
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from news.models import Post
from news.tasks import send_notifications, sender_emails
from django.contrib.auth.models import User
from Portal.celery import app


# @receiver(m2m_changed, sender=PostCategory)
# def notify_new_post(sender, instance, **kwargs):
# """сигнал уведомление о выходе новой статьи через промежуточную модель"""
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#             subscribers = [s.email for s in subscribers]
#
#             send_notifications.apply_async(
#                 (instance.preview(), instance.pk, instance.title, subscribers, instance.id),
#                 countdown=10
#             )


@receiver(post_save, sender=Post)
def notify_about_new_post(sender, instance, created, **kwargs):
    """сигнал уведомление о выходе новой статьи через post_save"""
    if created and instance.__class__.__name__ == 'Post':
        send_notifications.apply_async(
            (instance.preview(), instance.pk, instance.title),
            countdown=10)


@receiver(post_save, sender=User)
def send_email_after_register(sender, instance, created, **kwargs):
    if created:
        sender_emails.delay(account_id=instance.id)


@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    # отправляется письмо пользователю, чья почта была подтверждена
    send_mail(
        subject=f'Привет {email_address.user} Добро пожаловать на News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='NewsPortalDjango@yandex.ru',
        recipient_list=[email_address.user.email]
    )
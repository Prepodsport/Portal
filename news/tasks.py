from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from gevent.events import subscribers
from news.models import Post, Category, User

last_week = datetime.now() - timedelta(days=7)
posts = Post.objects.filter(date_time__gte=last_week)
categories = set(posts.values_list("category__name", flat=True))
subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))


@shared_task
def weekly_newsletter():
    """ таска новости за неделю """
    html_content = render_to_string(
        'week_notify.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_notifications(preview, pk, title):
    """ таска о выходе новой статьи/новости """
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}/'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


# @shared_task
# def user_signed_up(request, email_address, **kwargs):
#     # отправляется письмо пользователю, чья почта была подтверждена
#     send_mail(
#         subject=f'Привет {email_address.user} Добро пожаловать на News Portal!',
#         message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
#         from_email='NewsPortalDjango@yandex.ru',
#         recipient_list=[email_address.user.email]
#     )
@shared_task
def sender_emails(account_id):
    user = User.objects.get(id=account_id)

    send_mail(
        'Register',
        'Дорогой друг, спасибо за регистрацию на нашем сайте.',
        'NewsPortalDjango@yandex.ru',
        [user.email],
        fail_silently=False,
    )

import logging
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Reply
from ..board.settings import SITE_URL


def send_notifications(text, pk, title, subscribers):
    html_content = render_to_string(
        'news/post_created.html',
        {
            'text': text,
            'link': f'{SITE_URL}/ads/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='Tailingen1@yandex.ru',
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_ad_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.text, instance.pk, instance.title, subscribers)

logger_debug_one = logging.getLogger("debug_one")

@receiver(post_save, sender=Reply)
def comment_notice(sender, instance: Reply, created, **kwargs):
    """
    Если комментарий был одобрен или удален,
    отправляет автору уведомление на почту.
    """
    if not created:
        if instance.send_approved_notice():
            logger_debug_one.info(f'approve send {instance} email {instance.user.user.email}')
            send_mail(
                subject=f'Fun board. Одобрение отклика {instance.id}',
                message=f'Ваш отклик на статью {instance} одобрен.',
                from_email='',
                recipient_list=[instance.user.user.email]
            )
            instance.approved_notice_sended()

        if instance.send_deleted_notice():
            logger_debug_one.info(f'delete send {instance} sender {instance.user.user.email}')
            send_mail(
                subject=f'Fun board.  Удаление отклика {instance.id}',
                message=f'Ваш отклик на статью {instance} удален.',
                from_email='',
                recipient_list=[instance.user.user.email]
            )
            instance.delete_notice_sended()
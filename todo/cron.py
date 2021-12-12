from django.core.mail import send_mail
from django.utils import timezone
from . models import Remainder

def scheduled_task():
    unsent = Remainder.objects.filter(time__lte = timezone.now(), sent = False)
    if len(unsent) > 0:
        for mail in unsent:
            send_mail(
    'Remainder from Mini Tasks ',
    '<h2>Remainder that you set on mini tasks on ' + str(mail.added.date()) + '</h2> <p>' + str(mail.text),
    'Remainder@mini_tasks.com',
    [mail.mail],
    fail_silently=False,
)
        mail.sent = True
        mail.save()
    return True

scheduled_task()
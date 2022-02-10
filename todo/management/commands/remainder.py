from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from todo.models import Remainder

class Command(BaseCommand):
    help = 'Checks for unsent remainder and sends it if the time has passed.'

    def handle(self, *args, **kwargs):
        unsent = Remainder.objects.filter(time__lte = timezone.now(), sent = False)
        print(unsent)
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
        print("sent")
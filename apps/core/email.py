from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

def enviarMail(tipo, asunto, destino, url):
    
    context = {
        'tipo': tipo,
        'url': url
    }

    html = render_to_string('mail.html', context)

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [destino,]
    subject = asunto
    message = 'mensaje'

    send_mail(subject, message, from_email, recipient_list, html_message=html)

    return True
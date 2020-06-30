from django.shortcuts import render, redirect
from accounts.forms import SignUpWithEmailForm
from django.core.mail import send_mail
from django.conf import settings
import uuid


def d3demo(request):
    return render(request, 'd3demo.html')


# a email-sending script, not a view
def send_password_email(subject, message, recipient):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(e)


def index(request):
    if request.method == 'POST':
        form = SignUpWithEmailForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = email[0:email.index('@')]
            user.username = username
            random_uuid_password = uuid.uuid4().hex[0:6]
            user.set_password(random_uuid_password)
            user.save()
            # send a random uuid password email
            recipient = f'{email}'
            subject = "[Hololink] You have created an account."
            try:
                if '_' in username:
                    username_readable = ' '.join([word[0].upper() + word[1:] for word in username.split('_')])
                else:
                    username_readable = username
            except Exception:
                username_readable = username
            message = f'Hi {username_readable},'
            message += '\n\nYou have created a new account on Hololink. Login and learn more!'
            message += f'\n\nYour account: {username}'
            message += f'\nYour password: {random_uuid_password}'
            message += '\n\nSincerely,'
            message += '\nHololink'
            send_password_email(
                subject=subject,
                message=message,
                recipient=recipient,
            )
            return redirect('/accounts/password_reset/done/')
    else:
        form = SignUpWithEmailForm()
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)

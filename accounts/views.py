import os
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse

FROM_EMAIL = os.environ.get('FROM_EMAIL')

print('loading accounts view module')

def send_login_email(request):
    email = request.POST['email']
    print(f'sending email view: sending to {email}')
    token = Token.objects.create(email=email)
    login_url = request.build_absolute_uri( 
        reverse('login') + f'?token={str(token.uid)}'
    )
    email_body = f'Use this link to log in: {login_url}' 
    send_mail(
        'Your login link for Superlists',
        email_body,
        FROM_EMAIL,
        [email]
    )
    messages.success(request, "Check your email, we've sent you a link you can use to log in.")
    return redirect('/')

def login(request):
    print(f'login attempt')
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        print(f'loggin user in: user {user.email}')
        auth.login(request, user)
    return redirect('/')

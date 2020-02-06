import os
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse

FROM_EMAIL = os.environ.get('FROM_EMAIL')

def send_login_email(request):
    email = request.POST['email']
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
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

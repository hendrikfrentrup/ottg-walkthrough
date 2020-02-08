import os
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse
import time

FROM_EMAIL = os.environ.get('FROM_EMAIL')

current_pid = os.getpid()
print(f'loading accounts view module (PID:{current_pid})')

def send_login_email(request):
    start = time.time()
    print(f'sending email view (time: {time.time()-start}) PID:{current_pid}')
    email = request.POST['email']
    print(f'**sending to {email} (time: {time.time()-start}) PID:{current_pid}')
    token = Token.objects.create(email=email)
    print(f'**token created {token.uid} (time: {time.time()-start}) PID:{current_pid}' )
    login_url = request.build_absolute_uri( 
        reverse('login') + f'?token={str(token.uid)}'
    )
    print(f'**url generated {login_url} (time: {time.time()-start}) PID:{current_pid}')
    email_body = f'Use this link to log in: {login_url}' 
    print(f'**attempting to send mail (time: {time.time()-start}) PID:{current_pid}')
    send_mail(
        'Your login link for Superlists',
        email_body,
        FROM_EMAIL,
        [email]
    )
    print(f'**success sending mail (time: {time.time()-start}) PID:{current_pid}')
    messages.success(request, "Check your email, we've sent you a link you can use to log in.")
    print(f'**redirecting.. (time: {time.time()-start})')
    return redirect('/')

def login(request):
    print(f'login attempt')
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        print(f'loggin user in: user {user.email}')
        auth.login(request, user)
    return redirect('/')

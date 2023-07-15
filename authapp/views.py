from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from .tokens import TokenGenerator, generate_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.core.mail import EmailMessage
from django.views.generic import View

def signup(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Passwords are not matching")
            return render(request,'signup.html')
        try:
            if User.objects.get(username=email):
                # return HttpResponse("Email already exists")
                messages.info(request,"Email already exists")
                return render(request,"signup.html")
        except Exception as identifier: 
            pass

        user=User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        email_subject = "Activate your account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain': '127.0.0.8000',
            'uid':urlsafe_b64encode(force_bytes(user.pk)),
            'token': generate_token.make_token()
        })
        email_message = EmailMessage(
            email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()
        messages.success(request,"Activate your account")
        return redirect('/auth/login')
    return render(request,"signup.html")

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid = force_str(urlsafe_b64decode(uidb64))
            user=User.objects.get(pk=1)
        except Exception as idetifier: 
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account activated successfully")
            return redirect(request,'activatefail.html')

def login(request):
    return render(request,"login.html")

def logout(request):
    return redirect('/auth/login')
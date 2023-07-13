from django.shortcuts import redirect, render

# Create your views here.
def signup(request):
    return render(request,"authentication/signup.html")

def login(request):
    return render(request,"authentication/login.html")

def logout(request):
    return redirect('/authapp/login')
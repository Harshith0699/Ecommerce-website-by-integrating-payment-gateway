from django.urls import path
from authapp import views


urlpatterns = [
    path('signup/' , views.signup,name="signup"),
    path('login/' , views.handlelogin,name="signin"),
    path('logout/' , views.handlelogout,name="logout"),
    path('activate/<uidb64>/<token>' ,views.ActivateAccountView.as_view(),name="activate"),
]
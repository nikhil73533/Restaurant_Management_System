from django.urls import path,include
from . import views 
from  django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
urlpatterns = [
    path('',views.Home,name = "Home"),
    path('register',views.Register,name = "Register"),
    path('login',views.Login,name = "Login"),
    path('logout',views.Logout,name = "Logout"),
    path('profile',views.Profile,name = "Profile"),
    
     #Password Reset Urls

    path('reset_password/',PasswordResetView.as_view(template_name = "user/Password_email.html"),name = 'reset_password'),
    path('reset_password_sent/',PasswordResetDoneView.as_view(template_name = "user/Password_Reset_done.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name = "user/Password_Reset_confirm.html"), name = "password_reset_confirm"),
    path('reset_password_complete/',PasswordResetCompleteView.as_view(template_name = "user/Password_reset_submit.html"), name = "password_reset_complete"),

] 

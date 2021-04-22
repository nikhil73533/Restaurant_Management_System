from django.urls import path,include
from . import views 
from  django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Home,name = "Home"),
    path('register',views.Register,name = "Register"),
    path('login',views.Login,name = "Login"),
    path('logout',views.Logout,name = "Logout"),
] 
#Testing to see if pull request can be generated

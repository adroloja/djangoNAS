from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.index, name="index"),
   path('upload', views.handleMultipleImagesUpload, name="upload"),
   path('login', auth_views.LoginView.as_view(template_name="login.html"), name = "login"),
   path("signup", views.SignUpView.as_view(), name="signup"),
]

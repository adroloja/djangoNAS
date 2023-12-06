from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.index, name="index"),
   path('descargar', views.descargar, name="descargar"),
   path('upload', views.handleMultipleImagesUpload, name="upload"),
   path('login', auth_views.LoginView.as_view(template_name="login.html"), name = "login"),
   path("signup", views.SignUpView.as_view(), name="signup"),
   path('descargar_imagen/<int:image_id>/', views.descargar_imagen, name='descargar_imagen'),
   path('descargar_todo/', views.descargar_todo, name='descargar_todo'),

   ]

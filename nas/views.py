from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse 
from .models import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
# Create your views here.

def index(request):
   user = request.user
   return render(request, 'index.html', {'user' : user})

def handleMultipleImagesUpload(request):
    if request.method == "POST":
        images = request.FILES.getlist("fotos")
        for image in images:
            Image.objects.create(user=request.user, image = image)
        uploaded_images = Image.objects.filter(user = request.user)
        return JsonResponse({"images": [{"url": image.image.url} for image in uploaded_images]})
    return render(request, "index.html")

def create_user(username, email, password):
      user = User.objects.create_user(username=username, email=email, password=password)
      return user

def login_user(request, username, password):
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        return render(request, 'index.html', {"user" : user})
    else:
        return HttpResponse("Usuario no válido")
 
class SignUpView(FormView):
   template_name = 'signup.html'
   form_class = UserCreationForm
   success_url = reverse_lazy('index')

   def form_valid(self, form):
       user = form.save()
       login(self.request, user)
       return super().form_valid(form)
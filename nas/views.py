from io import BytesIO
from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Image
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import os
import zipfile

# Create your views here.

def index(request):
   user = request.user
   return render(request, 'index.html', {'user' : user})

@login_required
def descargar(request):
    images = Image.objects.filter(user = request.user)
    paginator = Paginator(images, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "descargar.html", {"user": request.user, "images" : images, "page_obj": page_obj})

def handleMultipleImagesUpload(request):
    if request.method == "POST":
        images = request.FILES.getlist("fotos")
        for image in images:
            Image.objects.create(user=request.user, image = image)
        uploaded_images = Image.objects.filter(user = request.user)
        #return JsonResponse({"images": [{"url": image.image.url} for image in uploaded_images]})
        return render(request, "index.html")
    return render(request, "index.html")

def descargar_imagen(request, image_id):
   image = Image.objects.get(pk=image_id)
   return FileResponse(open(image.image.path, 'rb'), content_type='image/jpeg')

def descargar_todo(request):
  images = Image.objects.filter(user=request.user.pk)
  if not images:
      return HttpResponse("No hay imágenes para descargar.")

  # Crear un archivo ZIP en memoria
  in_memory = BytesIO()

  # Crear el archivo ZIP
  with zipfile.ZipFile(in_memory, 'w') as zip_file:
      for image in images:
          # Añadir cada imagen al archivo ZIP
          zip_file.write(image.image.path, os.path.basename(image.image.path))

  # Mover el cursor al principio del archivo ZIP
  in_memory.seek(0)

  # Crear una respuesta con el archivo ZIP
  response = FileResponse(in_memory, content_type='application/zip')
  response['Content-Disposition'] = 'attachment; filename=images.zip'

  return response

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
   success_url = reverse_lazy('index.html')

   def form_valid(self, form):
       user = form.save()
       login(self.request, user)
       return super().form_valid(form)
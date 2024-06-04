import dataclasses
from telnetlib import LOGOUT
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import *


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}")
        print(f"Password: {password}")

        user = authenticate(request, email=email, password=password)
        print(f"User: {user}")

        if user is not None:
            login(request, user)
            return redirect('pocetna')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


@login_required
def pocetna_view(request):
    objave_posla = ObjavaPosla.objects.all().order_by('-datum_objave') 

    objave_posla_count = objave_posla.count() 

    margin_top_pixels = objave_posla_count * 50
    margin_top_pixels1 = objave_posla_count * 200
    margin_top_pixels2 = objave_posla_count * 430
    poslovi = Posao.objects.all()
    user = request.user  


   
    user = request.user  
  
   

    if hasattr(user, 'tvrtka') and user.tvrtka:
        user_role = 'Tvrtka'
    elif hasattr(user, 'freelancer') and user.freelancer:
        user_role = 'Freelancer'
    else:
        user_role = 'Unknown'

    if user_role == 'Tvrtka':
        template_name = 'tvrtka_pocetna.html'
    elif user_role == 'Freelancer':
        template_name = 'korisnik_pocetna.html'
    else:
        template_name = 'default_template.html'

    context = {
        'objave_posla': objave_posla,  
        'poslovi': poslovi,
        'objave_posla_count': objave_posla_count,  
        'margin_top_pixels': margin_top_pixels,  
        'margin_top_pixels1': margin_top_pixels1,  
        'margin_top_pixels2': margin_top_pixels2, 
    }

    return render(request, template_name, context)
@login_required
def ja_view(request):
    return render(request, 'ja.html')


@login_required
def create_objava_posla(request):  
    if request.method == 'POST':
        title = request.POST.get('inputNaslov')
        content = request.POST.get('inputObavijest')
        publication_date = date.today()
        expiration_date = date.today() + timedelta(days=30)
        posao_id = request.POST.get('inputPosao')  

        try:
            posao = Posao.objects.get(pk=posao_id)
            objava_posla = ObjavaPosla.objects.create( 
                title=title,
                content=content,
                publication_date=publication_date,
                expiration_date=expiration_date,
                posao=posao 
            )
            objava_posla.save()
            return redirect('pocetna')  
        except Kolegij.DoesNotExist:
            return redirect('pocetna') 

        return render(request, 'pocetna.html')

    @login_required
    def posao_list(request):
        kolegiji = Kolegij.objects.all()
     
        user = request.user  
        if hasattr(user, 'profesor') and user.profesor:
            user_role = 'Profesor'
        elif hasattr(user, 'admin') and user.admin:
            user_role = 'Admin'
        else:
            user_role = 'Unknown'

        if user_role == 'Profesor':
            template_name = 'profesor_kolegij.html'
        elif user_role == 'Admin':
            template_name = 'admin_kolegij.html'
        else:
            template_name = 'default_template.html'

        return render(request, template_name, {'kolegiji': kolegiji})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ObjavaPosla

@login_required
def get_objava_posla_view(request, obavijest_id):
    objavaPosla = get_object_or_404(ObjavaPosla, id=obavijest_id)
    data = {
        'id': objavaPosla.id,
        'title': objavaPosla.naslov,
        'content': objavaPosla.sadrzaj,
    }
    return JsonResponse(data)


@login_required
def edit_objava_posla_view(request, obavijest_id):
    objava_posla = get_object_or_404(ObjavaPosla, id=obavijest_id)

    if request.method == 'POST':
        updated_title = request.POST.get('updated_title')
        updated_content = request.POST.get('updated_content')

        objava_posla.naslov = updated_title
        objava_posla.sadrzaj = updated_content
        objava_posla.save()

        return redirect('pocetna')

    return JsonResponse({'id': objava_posla.id, 'title': objava_posla.naslov, 'content': objava_posla.sadrzaj})
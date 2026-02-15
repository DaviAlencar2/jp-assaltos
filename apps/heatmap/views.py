from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Robbery
from .geocode.geocode import geocode_address
from django.contrib import messages
from .forms import RobberyForm
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date


def ping(request): # Para o cronjob fazer request em manter o projeto 'acordado' no render.    
    return JsonResponse({'status': 'ok', 'authenticated': request.user.is_authenticated})


def is_staff(user):
    return user.is_authenticated and user.is_staff


def home(request):
    years = Robbery.objects.dates('date', 'year')
    years = [year.year for year in years]
    years.sort(reverse=True)
    current_year = str(date.today().year)

    context = {
        'years': years,
        'title': 'Home',
        'current_year': current_year,
    }

    return render(request, "heatmap/home.html", context)


@login_required(login_url='login')
def add(request):
    
    if request.method == "POST":
        messages.info(request, 'A API de geocodificação pode cometer erros de marcação leves, o mais importante é que o bairro esteja correto.')
        form = RobberyForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            street = form.cleaned_data['street']
            number = form.cleaned_data['number'] if form.cleaned_data['number'] else None
            neighborhood = form.cleaned_data['neighborhood']
            description = form.cleaned_data['description']
            location = f"{street}, {number} - {neighborhood.name}"
            latitude, longitude = geocode_address(location)

            if latitude is None or longitude is None:
                messages.error(request, 'Erro ao encontrar a localização. Verifique o endereço.')
                return render(request, "heatmap/add.html", {'form': form})

            robbery = Robbery(
                date=date,
                time=time,
                street=street,
                number=number,
                neighborhood=neighborhood,
                description=description,
                latitude=latitude,
                longitude=longitude,
                is_valid=False,  
                user=request.user,
            )

            robbery.save()
            messages.success(request, 'Dados adicionados com sucesso!')
            return redirect('home')
        
        else:
            messages.error(request, 'Erro ao adicionar dados. Verifique o formulário.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, "heatmap/add.html", {'form': form})
        
    elif request.method == "GET":
        form = RobberyForm(request.POST)
        return render(request, "heatmap/add.html", {'form': form})


def data_by_year(request, year):
    robberies_list = Robbery.objects.filter(date__year=year)
    data = []

    for robbery in robberies_list:
        data.append({
            'Latitude': str(robbery.latitude),
            'Longitude': str(robbery.longitude),
            'Data': str(robbery.date),
            'Hora': str(robbery.time),
            'Rua': robbery.street,
            'Numero': robbery.number,
            'Bairro': robbery.neighborhood.name,
            'Descricao': robbery.description,
        })

    response = JsonResponse(data, safe=False)
    return response


@login_required(login_url='login')
def delete_robbery(request, robbery_id):
    if request.method == "GET":
        try:
            robbery = Robbery.objects.get(id=robbery_id)
            if request.user.is_staff or robbery.user == request.user:
                robbery.delete()
                messages.success(request, 'Roubo deletado com sucesso.')
            else:
                messages.error(request, 'Você não tem permissão para deletar este roubo.')
        except Robbery.DoesNotExist:
            messages.error(request, 'Roubo não encontrado.')
    return redirect('profile')
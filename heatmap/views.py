from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Robbery
from .geocode.geocode import geocode_address
from django.contrib import messages
from .forms import RobberyForm


def ping(request): # Para o cronjob fazer request em manter o projeto 'acordado' no render.
    return JsonResponse({'status': 'ok'})


def is_staff(user):
    return user.is_authenticated and user.is_staff


def home(request):
    years = Robbery.objects.dates('date', 'year')
    years = [year.year for year in years]
    return render(request, "heatmap/home.html", {'years': years})


def stats(request):
    return render(request, "heatmap/stats.html")


def add(request):
    if not is_staff(request.user):
        messages.warning(request, 'Por enquanto, apenas administradores podem adicionar dados.')
        return redirect('home')
    
    elif request.method == "POST":
        form = RobberyForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            street = form.cleaned_data['street']
            number = form.cleaned_data['number']
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
        })

    response = JsonResponse(data, safe=False)
    return response

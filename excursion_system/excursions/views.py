from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PasswordForm, ExcursionForm, SearchForm
from .models import Excursion

# Секретный пароль (в реальном проекте используйте настройки или базу данных)
SECRET_PASSWORD = "admin123"

def home(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == SECRET_PASSWORD:
                request.session['authenticated'] = True
                return redirect('excursions')
            else:
                messages.error(request, "Неверный пароль")
    else:
        form = PasswordForm()
    
    return render(request, 'home.html', {'form': form, 'message': "Это MVP заявочной системы"})

def excursions_view(request):
    if not request.session.get('authenticated'):
        return redirect('home')
    
    excursions = None
    
    if request.method == 'POST':
        if 'submit_proposal' in request.POST:
            form = ExcursionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Экскурсия успешно предложена!")
                return redirect('excursions')
        
        elif 'submit_search' in request.POST:
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                search_date = search_form.cleaned_data['search_date']
                excursions = Excursion.objects.filter(
                    start_date__lte=search_date,
                    end_date__gte=search_date
                )
    
    return render(request, 'excursions.html', {
        'form': ExcursionForm(),
        'search_form': SearchForm(),
        'excursions': excursions
    })

def excursions_view_old(request):
    # Проверка аутентификации
    if not request.session.get('authenticated'):
        return redirect('home')
    
    if request.method == 'POST':
        # Обработка формы предложения
        if 'submit_proposal' in request.POST:
            form = ExcursionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Экскурсия успешно предложена!")
                return redirect('excursions')
        
        # Обработка формы поиска
        elif 'submit_search' in request.POST:
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                city = search_form.cleaned_data['city']
                start_date = search_form.cleaned_data['start_date']
                end_date = search_form.cleaned_data['end_date']
                
                # Фильтрация экскурсий
                excursions = Excursion.objects.all()
                
                if city:
                    excursions = excursions.filter(city__icontains=city)
                if start_date:
                    excursions = excursions.filter(start_date__gte=start_date)
                if end_date:
                    excursions = excursions.filter(end_date__lte=end_date)
                
                return render(request, 'excursions.html', {
                    'form': ExcursionForm(),
                    'search_form': search_form,
                    'excursions': excursions
                })
    
    return render(request, 'excursions.html', {
        'form': ExcursionForm(),
        'search_form': SearchForm()
    })
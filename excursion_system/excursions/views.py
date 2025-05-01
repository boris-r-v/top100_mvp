from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import PasswordForm, ExcursionForm, SearchForm
from .models import Excursion
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font
from datetime import datetime

# Секретный пароль для доступа (в реальном проекте используйте Django auth)
SECRET_PASSWORD = "admin123"

def home(request):
    """Главная страница с вводом пароля"""
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

    # Обработка очистки результатов
    if request.method == 'POST' and 'clear_results' in request.POST:
        return render(request, 'excursions.html', {
            'form': ExcursionForm(),
            'search_form': SearchForm(),
            'page_obj': None
        })

    # Обработка формы предложения
    if request.method == 'POST' and 'submit_proposal' in request.POST:
        form = ExcursionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Экскурсия успешно предложена!")
            return redirect('excursions')

    # Инициализация формы поиска с GET-параметрами
    search_form = SearchForm(request.POST or request.GET or None)
    excursions = Excursion.objects.none()

    if request.method == 'GET' or (request.method == 'POST' and 'submit_search' in request.POST):
        if search_form.is_valid():
            city = search_form.cleaned_data.get('city')
            search_date = search_form.cleaned_data.get('search_date')
            
            excursions = Excursion.objects.all()
            
            if city:
                excursions = excursions.filter(city__icontains=city)
            
            if search_date:
                excursions = excursions.filter(
                    start_date__lte=search_date,
                    end_date__gte=search_date
                )

    paginator = Paginator(excursions, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'excursions.html', {
        'form': ExcursionForm(),
        'search_form': search_form,
        'page_obj': page_obj,
        'search_params': request.GET.urlencode()  # Передаем параметры поиска
    })

def export_excursions(request):
    """Экспорт экскурсий в Excel"""
    if not request.session.get('authenticated'):
        return redirect('home')
    
    # Получаем параметры поиска из URL
    city = request.GET.get('city', '')
    search_date = request.GET.get('search_date', '')
    
    # Фильтрация аналогично основной странице
    excursions = Excursion.objects.all()
    
    if city:
        excursions = excursions.filter(city__icontains=city)
    
    if search_date:
        try:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            excursions = excursions.filter(
                start_date__lte=search_date,
                end_date__gte=search_date
            )
        except ValueError:
            pass
    
    # Создаем Excel-файл
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Экскурсии"
    
    # Заголовки
    headers = [
        "Город", "Предприятие", "Контактное лицо", 
        "Телефон", "Email", "Дата начала", "Дата окончания"
    ]
    ws.append(headers)
    
    # Стиль для заголовков
    for cell in ws[1]:
        cell.font = Font(bold=True)
    
    # Данные
    for exc in excursions:
        ws.append([
            exc.city,
            exc.company,
            exc.full_name,
            exc.phone or "-",
            exc.email,
            exc.start_date.strftime("%d.%m.%Y"),
            exc.end_date.strftime("%d.%m.%Y")
        ])
    
    # Автоподбор ширины столбцов
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Подготовка ответа
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=excursions.xlsx'
    wb.save(response)
    
    return response
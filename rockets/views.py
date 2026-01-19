from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from .models import Rocket, Cosmodrome, Launch
from .forms import RocketForm, CosmodromeForm, LaunchForm, SearchForm


def home(request):
    """Главная страница"""
    rockets_count = Rocket.objects.count()
    cosmodromes_count = Cosmodrome.objects.count()
    launches_count = Launch.objects.count()
    recent_launches = Launch.objects.all()[:5]
    
    # Статистика по статусам запусков
    success_count = Launch.objects.filter(status='success').count()
    planned_count = Launch.objects.filter(status='planned').count()
    failure_count = Launch.objects.filter(status='failure').count()
    partial_count = Launch.objects.filter(status='partial').count()
    
    context = {
        'rockets_count': rockets_count,
        'cosmodromes_count': cosmodromes_count,
        'launches_count': launches_count,
        'recent_launches': recent_launches,
        'success_count': success_count,
        'planned_count': planned_count,
        'failure_count': failure_count,
        'partial_count': partial_count,
    }
    return render(request, 'rockets/home.html', context)


def search(request):
    """Глобальный поиск по всем моделям"""
    query = request.GET.get('query', '')
    rockets = []
    cosmodromes = []
    launches = []
    
    if query:
        rockets = Rocket.objects.filter(
            Q(name__icontains=query) |
            Q(manufacturer__icontains=query) |
            Q(country__icontains=query) |
            Q(description__icontains=query)
        )
        cosmodromes = Cosmodrome.objects.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )
        launches = Launch.objects.filter(
            Q(mission_name__icontains=query) |
            Q(payload__icontains=query) |
            Q(description__icontains=query) |
            Q(rocket__name__icontains=query) |
            Q(cosmodrome__name__icontains=query)
        )
    
    context = {
        'query': query,
        'rockets': rockets,
        'cosmodromes': cosmodromes,
        'launches': launches,
        'form': SearchForm(initial={'query': query}),
    }
    return render(request, 'rockets/search.html', context)


# === Ракеты ===

def rocket_list(request):
    """Список всех ракет с сортировкой"""
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    valid_sort_fields = ['name', 'manufacturer', 'country', 'rocket_type', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    
    order_prefix = '-' if order == 'desc' else ''
    rockets = Rocket.objects.all().order_by(f'{order_prefix}{sort_by}')
    
    context = {
        'rockets': rockets,
        'current_sort': sort_by,
        'current_order': order,
    }
    return render(request, 'rockets/rocket_list.html', context)


def rocket_detail(request, pk):
    """Детальная страница ракеты"""
    rocket = get_object_or_404(Rocket, pk=pk)
    launches = rocket.launches.all()[:10]
    return render(request, 'rockets/rocket_detail.html', {'rocket': rocket, 'launches': launches})


def rocket_create(request):
    """Создание новой ракеты"""
    if request.method == 'POST':
        form = RocketForm(request.POST)
        if form.is_valid():
            rocket = form.save()
            messages.success(request, f'Ракета "{rocket.name}" успешно добавлена!')
            return redirect('rocket_detail', pk=rocket.pk)
    else:
        form = RocketForm()
    return render(request, 'rockets/rocket_form.html', {'form': form, 'title': 'Добавить ракету'})


def rocket_edit(request, pk):
    """Редактирование ракеты"""
    rocket = get_object_or_404(Rocket, pk=pk)
    if request.method == 'POST':
        form = RocketForm(request.POST, instance=rocket)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ракета "{rocket.name}" успешно обновлена!')
            return redirect('rocket_detail', pk=rocket.pk)
    else:
        form = RocketForm(instance=rocket)
    return render(request, 'rockets/rocket_form.html', {'form': form, 'title': 'Редактировать ракету', 'rocket': rocket})


def rocket_delete(request, pk):
    """Удаление ракеты"""
    rocket = get_object_or_404(Rocket, pk=pk)
    if request.method == 'POST':
        name = rocket.name
        rocket.delete()
        messages.success(request, f'Ракета "{name}" успешно удалена!')
        return redirect('rocket_list')
    return render(request, 'rockets/rocket_confirm_delete.html', {'rocket': rocket})


# === Космодромы ===

def cosmodrome_list(request):
    """Список всех космодромов с сортировкой"""
    sort_by = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    
    valid_sort_fields = ['name', 'country', 'location', 'founded_year', 'is_active']
    if sort_by not in valid_sort_fields:
        sort_by = 'name'
    
    order_prefix = '-' if order == 'desc' else ''
    cosmodromes = Cosmodrome.objects.all().order_by(f'{order_prefix}{sort_by}')
    
    context = {
        'cosmodromes': cosmodromes,
        'current_sort': sort_by,
        'current_order': order,
    }
    return render(request, 'rockets/cosmodrome_list.html', context)


def cosmodrome_detail(request, pk):
    """Детальная страница космодрома"""
    cosmodrome = get_object_or_404(Cosmodrome, pk=pk)
    launches = cosmodrome.launches.all()[:10]
    return render(request, 'rockets/cosmodrome_detail.html', {'cosmodrome': cosmodrome, 'launches': launches})


def cosmodrome_create(request):
    """Создание нового космодрома"""
    if request.method == 'POST':
        form = CosmodromeForm(request.POST)
        if form.is_valid():
            cosmodrome = form.save()
            messages.success(request, f'Космодром "{cosmodrome.name}" успешно добавлен!')
            return redirect('cosmodrome_detail', pk=cosmodrome.pk)
    else:
        form = CosmodromeForm()
    return render(request, 'rockets/cosmodrome_form.html', {'form': form, 'title': 'Добавить космодром'})


def cosmodrome_edit(request, pk):
    """Редактирование космодрома"""
    cosmodrome = get_object_or_404(Cosmodrome, pk=pk)
    if request.method == 'POST':
        form = CosmodromeForm(request.POST, instance=cosmodrome)
        if form.is_valid():
            form.save()
            messages.success(request, f'Космодром "{cosmodrome.name}" успешно обновлён!')
            return redirect('cosmodrome_detail', pk=cosmodrome.pk)
    else:
        form = CosmodromeForm(instance=cosmodrome)
    return render(request, 'rockets/cosmodrome_form.html', {'form': form, 'title': 'Редактировать космодром', 'cosmodrome': cosmodrome})


def cosmodrome_delete(request, pk):
    """Удаление космодрома"""
    cosmodrome = get_object_or_404(Cosmodrome, pk=pk)
    if request.method == 'POST':
        name = cosmodrome.name
        cosmodrome.delete()
        messages.success(request, f'Космодром "{name}" успешно удалён!')
        return redirect('cosmodrome_list')
    return render(request, 'rockets/cosmodrome_confirm_delete.html', {'cosmodrome': cosmodrome})


# === Запуски/Миссии ===

def launch_list(request):
    """Список всех запусков с сортировкой"""
    sort_by = request.GET.get('sort', 'launch_date')
    order = request.GET.get('order', 'desc')
    
    valid_sort_fields = ['mission_name', 'rocket__name', 'cosmodrome__name', 'launch_date', 'status']
    if sort_by not in valid_sort_fields:
        sort_by = 'launch_date'
    
    order_prefix = '-' if order == 'desc' else ''
    launches = Launch.objects.all().order_by(f'{order_prefix}{sort_by}')
    
    context = {
        'launches': launches,
        'current_sort': sort_by,
        'current_order': order,
    }
    return render(request, 'rockets/launch_list.html', context)


def launch_detail(request, pk):
    """Детальная страница запуска"""
    launch = get_object_or_404(Launch, pk=pk)
    return render(request, 'rockets/launch_detail.html', {'launch': launch})


def launch_create(request):
    """Создание нового запуска"""
    if request.method == 'POST':
        form = LaunchForm(request.POST)
        if form.is_valid():
            launch = form.save()
            messages.success(request, f'Запуск "{launch.mission_name}" успешно добавлен!')
            return redirect('launch_detail', pk=launch.pk)
    else:
        form = LaunchForm()
    return render(request, 'rockets/launch_form.html', {'form': form, 'title': 'Добавить запуск'})


def launch_edit(request, pk):
    """Редактирование запуска"""
    launch = get_object_or_404(Launch, pk=pk)
    if request.method == 'POST':
        form = LaunchForm(request.POST, instance=launch)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запуск "{launch.mission_name}" успешно обновлён!')
            return redirect('launch_detail', pk=launch.pk)
    else:
        form = LaunchForm(instance=launch)
    return render(request, 'rockets/launch_form.html', {'form': form, 'title': 'Редактировать запуск', 'launch': launch})


def launch_delete(request, pk):
    """Удаление запуска"""
    launch = get_object_or_404(Launch, pk=pk)
    if request.method == 'POST':
        name = launch.mission_name
        launch.delete()
        messages.success(request, f'Запуск "{name}" успешно удалён!')
        return redirect('launch_list')
    return render(request, 'rockets/launch_confirm_delete.html', {'launch': launch})

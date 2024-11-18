from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ChildForm
from .models import Child
from .utils import generate_qr_code  # Импортируйте функцию генерации QR-кода

def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            generate_qr_code(child)  # Генерация QR-кода
            child.save()  # Сохранение ребёнка с QR-кодом
            return JsonResponse({'success': True, 'qr_code_url': child.qr_code.url})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    form = ChildForm()
    return render(request, 'children/add_child.html', {'form': form})




def main_view(request):
    # Список секций
    sections = [
        {'name': 'Бокс', 'url': '/section/boxing/'},
        {'name': 'Каратэ', 'url': '/section/karate/'},
        {'name': 'Дзюдо', 'url': '/section/judo/'},
        {'name': 'Борьба', 'url': '/section/wrestling/'},
    ]
    return render(request, 'children/main.html', {'sections': sections})


def boxing_view(request):
    students = [
        {'id': 1, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 2, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 3, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 4, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 5, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 6, 'name': 'Акимжанов Ануар Акимжанович'},
    ]
    return render(request, 'children/boxing.html', {'students': students})

def profile_view(request):
    return render(request, 'children/profile.html')

def scan_view(request):
    return render(request, 'children/scan.html')

def identify_child(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data', '')
        try:
            # Поиск ребенка по данным из QR-кода
            child = Child.objects.get(iin=qr_data.split(' ')[2])  # Пример: парсинг ИИН из текста QR-кода
            return JsonResponse({'success': True, 'child_name': child.full_name, 'birth_date': child.birth_date})
        except Child.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Ребёнок не найден.'})
    return JsonResponse({'success': False, 'error': 'Неверный метод запроса.'})


def add_new_child(request):
    return render(request, 'children/add_new_child.html')


def add_section(request):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        schedule = request.POST.get('schedule')
        time = request.POST.get('time')
        # Здесь вы можете сохранить данные в базу данных, если нужно.
        # Например:
        # Section.objects.create(name=section_name, schedule=schedule, time=time)
        return redirect('profile')  # Перенаправляем на страницу профиля после добавления
    
    return render(request, 'children/add_section.html')


def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        # Здесь можно добавить сохранение сотрудника в базу данных, если нужно:
        # Employee.objects.create(username=username, password=password, photo=photo)
        return redirect('profile')  # После добавления перенаправляем в профиль

    return render(request, 'children/add_employee.html')

def add_organization(request):
    if request.method == 'POST':
        organization_name = request.POST.get('organization_name')
        director_username = request.POST.get('director_username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Логика проверки паролей
        if password != confirm_password:
            return render(request, 'children/add_organization.html', {'error': 'Пароли не совпадают!'})
        
        # Сохранение организации в базу данных (опционально)
        # Organization.objects.create(name=organization_name, director=director_username, password=password)
        return redirect('profile')  # После добавления перенаправляем в профиль

    return render(request, 'children/add_organization.html')
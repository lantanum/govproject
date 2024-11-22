from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import generate_qr_code  # Импортир
import time

def main_view(request):
    # Список секций
    sections = [
        {'name': 'Бокс', 'url': '/section/boxing/'},
        {'name': 'Каратэ', 'url': '/section/karate/'},
        {'name': 'Дзюдо', 'url': '/section/judo/'},
        {'name': 'Борьба', 'url': '/section/wrestling/'},
    ]
    return render(request, 'myapp/main.html', {'sections': sections})


def boxing_view(request):
    students = [
        {'id': 1, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 2, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 3, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 4, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 5, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 6, 'name': 'Акимжанов Ануар Акимжанович'},
    ]
    return render(request, 'myapp/boxing.html', {'students': students})

def profile_view(request):
    return render(request, 'myapp/profile.html')

def scan_view(request):
    person = request.user.person  # Получение связанного объекта Person

    if person.role == 'client':
        # Генерация QR-кода для клиента
        if request.method == 'POST':
            qr_data = f"user:{request.user.username};time:{int(time.time())}"
            qr_code, expiration_time = generate_qr_code(qr_data)  # Функция генерации QR-кода
            return JsonResponse({'success': True, 'qr_code': qr_code, 'expiration_time': expiration_time})
        return render(request, 'myapp/scan.html')

    elif person.role == 'coach':
        # Страница для сканирования QR для тренера
        return render(request, 'myapp/scan_qr.html')

    # Ошибка доступа для других ролей
    return JsonResponse({'error': 'Доступ запрещён.'}, status=403)



def add_section(request):
    if request.method == 'POST':
        section_name = request.POST.get('section_name')
        schedule = request.POST.get('schedule')
        time = request.POST.get('time')
        # Здесь вы можете сохранить данные в базу данных, если нужно.
        # Например:
        # Section.objects.create(name=section_name, schedule=schedule, time=time)
        return redirect('profile')  # Перенаправляем на страницу профиля после добавления
    
    return render(request, 'myapp/add_section.html')


def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        # Здесь можно добавить сохранение сотрудника в базу данных, если нужно:
        # Employee.objects.create(username=username, password=password, photo=photo)
        return redirect('profile')  # После добавления перенаправляем в профиль

    return render(request, 'myapp/add_employee.html')

def add_organization(request):
    if request.method == 'POST':
        organization_name = request.POST.get('organization_name')
        director_username = request.POST.get('director_username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Логика проверки паролей
        if password != confirm_password:
            return render(request, 'myapp/add_organization.html', {'error': 'Пароли не совпадают!'})
        
        # Сохранение организации в базу данных (опционально)
        # Organization.objects.create(name=organization_name, director=director_username, password=password)
        return redirect('profile')  # После добавления перенаправляем в профиль

    return render(request, 'myapp/add_organization.html')
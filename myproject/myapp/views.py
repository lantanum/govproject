from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import generate_qr_code  # Импортир

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
            qr_code = generate_qr_code(qr_data)  # Функция генерации QR-кода
            return JsonResponse({'success': True, 'qr_code': qr_code})
        return render(request, 'myapp/scan.html')

    elif person.role == 'coach':
        # Страница для сканирования QR для тренера
        return render(request, 'myapp/scan_qr.html')

    # Ошибка доступа для других ролей
    return JsonResponse({'error': 'Доступ запрещён.'}, status=403)
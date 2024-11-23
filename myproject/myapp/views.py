from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import generate_qr_code  # Импортир
from .models import Section, Person, Attendance
import time
from datetime import date
from datetime import timedelta
from io import BytesIO

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
    person = request.user.person  # Получаем связанный объект Person

    if person.role == 'client':
        # Генерация QR-кода для клиента
        if request.method == 'POST':
            qr_data = f"user:{request.user.username};time:{int(time.time())}"
            return JsonResponse({'success': True, 'qr_data': qr_data})
        return render(request, 'myapp/scan.html')

    elif person.role == 'coach':
        # Страница для сканирования QR для тренера
        if request.method == 'POST':
            qr_data = request.POST.get('qr_data')
            # Парсим qr_data и находим информацию
            try:
                username = qr_data.split(';')[0].split(':')[1]
                user = User.objects.get(username=username)
                client_person = user.person  # Получаем Person клиента

                # Определяем первую секцию, связанную с организацией пользователя
                section = Section.objects.filter(organization=client_person.organization).first()

                if not section:
                    return JsonResponse({'success': False, 'error': 'Секция не найдена.'})

                # Создаем запись о посещении
                attendance = Attendance.objects.create(
                    person=client_person,
                    section=section,
                    visit_date=date.today()
                )

                return JsonResponse({
                    'success': True,
                    'message': f"Посещение за {date.today()} зарегистрировано для {client_person.user.username} на секции {section.name}"
                })

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return render(request, 'myapp/scan_qr.html')

    return JsonResponse({'error': 'Доступ запрещён.'}, status=403)

def mark_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data')
            visit_date = data.get('visit_date')

            if not qr_data or not visit_date:
                return JsonResponse({"success": False, "error": "Неверные данные."})

            # Преобразуем дату
            visit_date_parsed = parse_date(visit_date)

            # Получаем первую секцию, привязанную к пользователю
            section = Section.objects.filter(organization=request.user.person.organization).first()

            if section:
                # Создаем запись о посещении
                Attendance.objects.create(
                    user=request.user,
                    section=section,
                    visit_date=visit_date_parsed,
                    qr_data=qr_data
                )
                return JsonResponse({"success": True})

            return JsonResponse({"success": False, "error": "Не найдена секция для пользователя."})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Неверный метод запроса."})


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

import qrcode
from django.utils import timezone
import json
import base64

def generate_qr(request):
    if request.method == "POST":
        # Получаем текущую дату и добавляем срок действия для QR-кода (например, 10 минут)
        expiration_time = timezone.now() + timedelta(minutes=10)

        # Создаем данные для QR-кода
        qr_data = {
            "user_id": request.user.id,
            "expiration_time": expiration_time.isoformat()
        }

        # Генерируем QR-код
        qr = qrcode.make(json.dumps(qr_data))

        # Сохраняем QR-код в формате изображения
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)
        qr_code_base64 = base64.b64encode(img_io.read()).decode('utf-8')

        return JsonResponse({
            "success": True,
            "qr_code": qr_code_base64,
            "expiration_time": expiration_time.isoformat()  # Возвращаем время истечения
        })

    return JsonResponse({"success": False, "error": "Неверный запрос."})
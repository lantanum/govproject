from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from .utils import generate_qr_code  # Импортир
from .models import Organization, Section, Person, Attendance
import time
from datetime import date, datetime
from datetime import timedelta
from io import BytesIO
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now

def main_view(request):
    sections = []
    
    user_person = request.user.person
    
    if user_person.role == 'client':  # Для клиента показываем только его привязанные секции
        sections = Section.objects.filter(participants=user_person)  # Используем связь ManyToMany с участниками
    elif user_person.role in ['coach', 'director']:  # Для тренера и директора показываем все секции его организации
        organization = user_person.organization
        sections = Section.objects.filter(organization=organization)

    return render(request, 'myapp/main.html', {'sections': sections})


def section_attendance(request, section_id):
    section = Section.objects.get(id=section_id)
    selected_date = request.GET.get('date', None)

    # Получаем пользователя, чтобы определить его роль
    user = request.user
    person = user.person
    role = user.person.role  # Предположим, что роль хранится в профиле пользователя

    # Фильтрация посещений в зависимости от роли пользователя
    if role == "client":
        attendances = Attendance.objects.filter(person=user.person, section=section)
    else:
        # Для тренера и директора отображаются все посещения в данной секции
        attendances = Attendance.objects.filter(section=section)

    # Если выбрана дата, фильтруем по ней
    if selected_date:
        attendances = attendances.filter(visit_date=selected_date)

    return render(request, 'myapp/section_attendance.html', {
        'section': section,
        'attendances': attendances,
        'selected_date': selected_date
    })

def add_client(request):
    # Проверяем, что пользователь - тренер
    if not request.user.person.role == 'coach':
        raise PermissionDenied

    # Получаем организацию тренера
    coach_person = request.user.person
    organization = coach_person.organization

    # Получаем все секции в организации, доступные для тренера
    sections = Section.objects.filter(organization=organization)

    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')
        selected_sections = request.POST.getlist('sections')  # Секции, выбранные для клиента

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, password=password)

        # Роль "client" назначается автоматически после создания пользователя
        person = user.person
        person.role = 'client'  # Устанавливаем роль клиента
        person.organization = organization  # Привязываем его к организации тренера

        # Добавляем выбранные секции клиенту
        for section_id in selected_sections:
            section = Section.objects.get(id=section_id)
            person.sections.add(section)


        # Сохраняем изменения
        person.save()

        # Перенаправляем обратно на страницу профиля тренера
        return redirect('profile')

    return render(request, 'myapp/add_client.html', {'sections': sections})

def profile_view(request):
    user = request.user  # Получаем текущего пользователя
    try:
        # Получаем профиль пользователя
        person = Person.objects.get(user=user)
    except Person.DoesNotExist:
        person = None  # Если профиль не найден, можно задать пустое значение

    context = {
        'user': user,
        'person': person,
    }
    return render(request, 'myapp/profile.html', context)


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
    # Проверяем, что пользователь является тренером в организации
    if not request.user.person.role == 'director':
        raise PermissionDenied

    # Получаем организацию тренера
    coach_person = request.user.person
    organization = coach_person.organization

    if request.method == 'POST':
        # Получаем данные из формы
        section_name = request.POST.get('section_name')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Преобразуем строки в время
        try:
            start_time = datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.strptime(end_time, '%H:%M').time()

            # Создаем секцию
            section = Section.objects.create(
                name=section_name,
                start_time=start_time,
                end_time=end_time,
                organization=organization
            )

            # Перенаправляем на страницу профиля тренера
            return redirect('profile')

        except ValueError:
            # В случае ошибки при преобразовании времени
            return render(request, 'myapp/add_section.html', {'error': 'Неверный формат времени'})

    return render(request, 'myapp/add_section.html')


def add_employee(request):
    # Проверяем, что пользователь - директор организации
    if not request.user.person.role == 'director':
        raise PermissionDenied

    # Получаем организацию руководителя
    director_person = request.user.person
    organization = director_person.organization

    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username')
        password = request.POST.get('password')
        photo = request.FILES.get('photo')

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, password=password)

        # Роль "coach" назначается автоматически после создания пользователя
        person = user.person  # Получаем объект Person для нового пользователя
        person.role = 'coach'  # Устанавливаем роль сотрудника
        person.organization = organization  # Привязываем его к организации руководителя

        # Сохраняем изменения
        person.save()

        # Перенаправляем обратно на страницу профиля директора
        return redirect('profile')

    return render(request, 'myapp/add_employee.html')

def add_organization(request):
    if request.method == "POST":
        org_name = request.POST.get('organization_name')
        director_username = request.POST.get('director_username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Проверка на совпадение паролей
        if password != confirm_password:
            return render(request, 'myapp/add_organization.html', {'error': 'Пароли не совпадают'})

        # Проверка, существует ли пользователь с таким именем
        try:
            existing_user = User.objects.get(username=director_username)
            return render(request, 'myapp/add_organization.html', {'error': 'Пользователь с таким логином уже существует'})
        except User.DoesNotExist:
            # Если пользователь не найден, продолжаем создание нового пользователя
            pass

        # Создание пользователя для руководителя
        try:
            director_user = User.objects.create_user(username=director_username, password=password)
        except Exception as e:
            return render(request, 'myapp/add_organization.html', {'error': f'Ошибка создания пользователя: {str(e)}'})

        # Создание организации и связывание с пользователем
        with transaction.atomic():
            # Создаем организацию
            organization = Organization.objects.create(name=org_name)

            # Проверяем, существует ли уже профиль для этого пользователя
            if not Person.objects.filter(user=director_user).exists():
                # Создаем профиль для руководителя с ролью "director"
                person = Person.objects.create(
                    user=director_user,
                    role='director',  # Назначаем роль руководителя
                    organization=organization
                )
            else:
                # Если профиль уже существует, то просто обновляем организацию для пользователя
                person = Person.objects.get(user=director_user)
                person.organization = organization
                person.save()

            # Связываем директора с организацией, привязываем не User, а Person
            organization.director = person  # Здесь привязываем Person, а не User
            organization.save()

        # Сообщение об успешном создании
        messages.success(request, 'Организация успешно создана!')

        # Перенаправляем на страницу профиля
        return redirect('/myapp/profile/')  # Замените на нужный URL

    # Если это GET-запрос, показываем пустую форму
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
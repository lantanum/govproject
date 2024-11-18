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

def home(request):
    return render(request, 'children/home.html')
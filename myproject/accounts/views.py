from django.shortcuts import render

# Create your views here.
def main_view(request):
    # Список секций
    sections = [
        {'name': 'Бокс', 'url': '/section/boxing/'},
        {'name': 'Каратэ', 'url': '/section/karate/'},
        {'name': 'Дзюдо', 'url': '/section/judo/'},
        {'name': 'Борьба', 'url': '/section/wrestling/'},
    ]
    return render(request, 'accounts/main.html', {'sections': sections})


def boxing_view(request):
    students = [
        {'id': 1, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 2, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 3, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 4, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 5, 'name': 'Акимжанов Ануар Акимжанович'},
        {'id': 6, 'name': 'Акимжанов Ануар Акимжанович'},
    ]
    return render(request, 'accounts/boxing.html', {'students': students})
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import FileForm
from cnn.image_processing import generate_title, get_face
from cnn.predict_gender import predict


def home(request):
    """Загружаем фотографию"""
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('result', kwargs={'title': form.cleaned_data['title']}))
    else:
        form = FileForm(initial={'title': generate_title()})
    return render(request, 'predictor/home.html', {'form': form})


def result(request, title):
    """Выдеяем лицо на фотографии"""
    context = get_face(title)
    if context['result']:
        result = predict(title)
        context.update({'gender': result})
    return render(request, 'predictor/result.html', context)

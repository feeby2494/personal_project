from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'simple_app/index.html', {})

def bingo(request):
    return render(request, 'simple_app/bingo.html', {})

def bmi(request):
    return render(request, 'simple_app/bmi.html', {})
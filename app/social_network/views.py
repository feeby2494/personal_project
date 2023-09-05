from django.shortcuts import render

# Create your views here.
def indexSocial(request):
    return render(request, 'social/index.html', {})

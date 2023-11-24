from django.shortcuts import render

# Create your views here.
def indexMap(request):
    return render(request, 'route_map/index.html', {})
from django.http import HttpResponse
from django.shortcuts import redirect, render
import datetime

from django.contrib.auth.decorators import login_required

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

@login_required(login_url='/accounts/login')
def profile(request):
    # double check if user is authenticated
    if request.user.is_authenticated:

        # want to filter by group
        my_groups = [obj['name'] for obj in request.user.groups.all().values('name')]

        return render(request, 'parent/profile.html', {'my_groups': my_groups})
    else:
        return redirect('/accounts/login')
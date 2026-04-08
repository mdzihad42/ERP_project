from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    page = request.GET.get('page', 'Overview')
    return render(request, 'hr/dashboard.html', {'page': page})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notifications

def working(request):
    return render(request, 'otherpages/working.html')

@login_required
def notifications(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'otherpages/notifications.html', {'notifications':notifications})
from django.shortcuts import render

def working(request):
    return render(request, 'otherpages/working.html')
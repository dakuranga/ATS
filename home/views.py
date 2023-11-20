from django.shortcuts import render

def myview(request):
    return render(request, 'myview.html')

def todayview(request):
    return render(request, 'today.html')

def dashboardview(request):
    return render(request, 'dashboard.html')
